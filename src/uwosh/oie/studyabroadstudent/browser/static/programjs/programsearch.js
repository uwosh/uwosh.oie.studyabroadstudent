require([
  '++plone++uwosh.oie.studyabroadstudent/libs/react/react.min',
], function(R) {
  var D = R.DOM;

  var ProgramSearchComponent = R.createClass({
      getInitialState: function(){
        return {
          filters: {...this.props.defaultFilters},
          markers: [],
          currentPage: 1,
          perPage: 12,
          activePrograms: [...this.props.programs],
        };
      },

      getDefaultProps: function(){
        const el = document.getElementById('oie-search');
        const program_data = el.getAttribute('oie-program-data');
        const programs = JSON.parse(program_data);
        console.log('programs')
        console.log(programs)
        const titles = [
          ...new Set(
            programs.map(program=>program.title)
          )
        ];
        const years = [
          ...new Set(
            programs.map(program=>program.calendarYear)
          )
        ];
        const types = [
          ...new Set(
            programs.map(program=>program.type)
          )
        ];
        const countries = [
          ...new Set(
            programs.flatMap(program=>program.countries)
          )
        ];
        const terms = [
          ...new Set(
            programs.flatMap(program=>program.term)
          )
        ];
        const colleges = [
          ...new Set(
            programs.flatMap(program=>program.college)
          )
        ];
        const leaders = [
          ...new Set(
            programs.flatMap(program=>program.leader)
          )
        ];
        const noMatchingPrograms = D.div(
          {},
          [ D.span({}, ['No Matching Programs'])]
        );
        return {
          programs,
          titles,
          years,
          terms,
          leaders,
          colleges,
          types,
          countries,
          noMatchingPrograms,
          portal_url: document.body.getAttribute('data-portal-url'),
          defaultFilters: {
            type: false,
            title: null,
            calendarYear: false,
            countries: false,
            term: false,
            college: false,
            leader: false,
          },
          nullValues: [
            null,
            'null',
            'N/A',
            'n/a',
            'na',
            ''
          ],
          trueValues: [
            true,
            'true',
            'True',
            'Yes',
            'yes',
            'Y',
            'y'
          ],
        };
      },

      getActiveProgramCount: function(){
        return this.state.activePrograms.length;
      },

      render: function(){
        return D.div({}, [
          D.form(
            {
              onKeyPress: this.handleKeyPress,
              id: 'oie-search-form'
            },
            this.renderSearchFields(),
          ),
          this.renderPrograms(),
        ]);
      },

      handleKeyPress(event){
        if(event.key === 'Enter' && !(event.target.classList.contains('clear-button'))){
          event.preventDefault();
          this.handler(event);
        }
      },

      getDefaultOption: function(selectionName){
        return D.option(
          { selected: true, value: 'n/a' },
          `--Select a ${selectionName}--`,
        );
      },

      getOptions: function(optionsList, optionsName){
        return [
          this.getDefaultOption(optionsName),
          ...optionsList
            .filter(value => !this.props.nullValues.includes(value))
            .map(value => D.option(
            { value },
            value,
          )),
        ];
      },

      renderSearchFields: function(){
        const titleField = D.input({
          className: 'form-control oie-search-field',
          type: 'text',
          name: 'title',
          placeholder: 'Program Name/Title',
          onChange: this.handler.bind(this),
        });

        const countryField = D.select(
          {
            className: 'form-control oie-search-field',
            name: 'countries',
            onChange: this.handler.bind(this),
          },
          this.getOptions(this.props.countries, 'Program Country')
        );

        const typeField = D.select(
          {
            className: 'form-control oie-search-field',
            name: 'type',
            onChange: this.handler.bind(this),
          },
          this.getOptions(this.props.types, 'Program Type'),
        );

        const collegeField = D.select(
          {
            className: 'form-control oie-search-field',
            name: 'college',
            onChange: this.handler.bind(this),
          },
          this.getOptions(this.props.colleges, 'Program College'),
        );

        const termField = D.select(
          {
            className: 'form-control oie-search-field',
            name: 'term',
            onChange: this.handler.bind(this),
          },
          this.getOptions(this.props.terms, 'Program Term')
        );

        const yearField = D.select(
          {
            className: 'form-control oie-search-field',
            name: 'calendarYear',
            onChange: this.handler.bind(this),
          },
          this.getOptions(this.props.years, 'Program Year')
        );

        const leaderField = D.select(
          {
            className: 'form-control oie-search-field',
            name: 'leader',
            onChange: this.handler.bind(this),
          },
          this.getOptions(this.props.leaders, 'Program Leader')
        );


        const clearButton = D.button({
          className: 'btn btn-primary clear-button',
          onClick: this.resetSearchFields
        }, 'Clear');

        return [
          titleField,
          countryField,
          typeField,
          collegeField,
          termField,
          yearField,
          leaderField,
          clearButton,
        ];
      },

      handler: function(event){
        event.preventDefault();
        console.log(event)
        const {checked, value, name, type} = event.target;
        const actualValue = type === 'checkbox' ? checked : value;
        const filters = {
          ...this.state.filters,
          [name]: actualValue,
        };
        const activePrograms = this.getFilteredResults(filters);
        this.setState({
          filters,
          activePrograms,
        });
      },

      getForm: function() {
        return document.getElementById('oie-search-form');
      },

      resetSearchFields: function(event){
        console.log(event)
        event.preventDefault();
        this.getForm().reset();
        const filters = {...this.props.defaultFilters};
        this.setState({
          filters,
          activePrograms: this.getFilteredResults(filters),
        });
      },

      filtersMatch: function(filterName, filterValue, program){
        const actualValue = program[filterName];
        if(
          this.props.nullValues.includes(filterValue) ||
          this.props.nullValues.includes(actualValue)
          ){
          return true;
        }
        console.log('typeof filterValue')
        console.log(typeof filterValue)
        switch(typeof filterValue){
          case 'boolean':
            return filterValue === false || this.props.trueValues.includes(actualValue); //this might be a mistake?
          case 'string':
            const searchValue = filterValue.toLowerCase().trim();
            const actualValues = [actualValue].flatMap(el=>el);
            return actualValues
              .map(value => value.toLowerCase().trim())
              .some(value => value.includes(searchValue));
          default:
            return false;
        }
      },

      getFilteredResults: function(filters=this.state.filters){
        return Object.entries(filters)
          .reduce(
            (remainingPrograms, [filterName, filterValue]) => {
              return remainingPrograms.filter(
                program => this.filtersMatch(filterName, filterValue, program)
              );
            },
            this.props.programs,
          );
      },

      getPagingIndices: function(){
        const startingIndex = this.state.perPage * (this.state.currentPage - 1);
        return [
          startingIndex,
          Math.min(
            startingIndex + this.state.perPage,
            this.getActiveProgramCount(),
          ),
        ];
      },

      getProgramViews: function() {
        const views = this.state.activePrograms
          .slice(...this.getPagingIndices())
          .map(program => {
            const imgSrc = program.image || '/oie/++theme++oie-study-abroad-theme/img/logo.png';
            const title = D.div(
              {className: 'search-program-title'},
              D.a({href: program.url}, program.title),
            );
          const programImage = D.div(
            {className: 'image-container'},
            [D.img({
                className: 'search-program-image focuspoint',
                alt: '',
                src: imgSrc
              })]
            );
            const description = D.p(
              {className: 'search-program-description'},
              program.description,
            );
            const more = D.a(
              { className: 'search-program-link', href: program.url },
            'More...',
            );
            return D.div(
              { className: 'search-program-view col-lg-2 col-md-3 col-sm-4' },
              D.div(
                { className: 'program-margin' },
                [
                  title,
                  programImage,
                  description,
                  more,
                ],
              ),
            );
          });
        return D.div(
          { className: 'program-group col-xs-12' },
          views,
        );
      },

      renderPrograms: function(){
        const activeProgramCount = this.getActiveProgramCount();
        if (activeProgramCount === 0) {
          return this.props.noMatchingPrograms;
        }
        return D.div(
          { className: 'program-listing' },
          [
             D.span(
              { className: 'oie-search-counter col-xs-12' },
              `${activeProgramCount} programs(s) found`,
            ),
            this.getProgramViews(),
            this.renderPaging(),
          ],
        );
      },

      getPageCount: function(){
        return Math.ceil(this.getActiveProgramCount() / this.state.perPage);
      },

      onPageClick: function(event) {
        event.preventDefault();
        const page = parseInt(event.target.target)
        if (page > 0 && page <= this.getPageCount()){
          this.setState({ page });
        }
      },

      renderPage: function(number, label) {
        const outOfBounds = number < 1 || number > this.getPageCount()
        if(outOfBounds && !label){
          return;
        }
        label = label || number;
        const currentClass = number === this.state.page ? ' current' : '';
        const disabledClass = outOfBounds ? ' disabled' : '';
        const className = `page-item${currentClass}${disabledClass}`
        return D.li(
          { className },
          D.a(
            {
              onClick: this.onPageClick.bind(this),
              href: number,
              target: number,
              className: 'page-link'
            },
            label,
          ),
        );
      },

      renderNumberedPages: function(){
        return [...Array(10).keys()] // [0, 1, 2,..., 9]
          .map(el => el + this.state.currentPage) // make first element the current page number
          .map(el => el - 2) // make array start with two previous page numbers
          .filter(el => el > 0 && el <= this.getPageCount()) // remove pages that don't make sense
          .slice(0, 8) // get max of 8 pages
          .map(el => this.renderPage(el))
      },

      renderPaging: function() {
        return D.div(
          { className: 'oie-paging' },
          D.ul(
            { className: 'pagination' },
            [
              this.renderPage(1, 'First'),
              this.renderPage(this.state.currentPage - 1, 'Prev'),
              ...this.renderNumberedPages(),
              this.renderPage(this.state.currentPage + 1, 'Next'),
              this.renderPage(this.getPageCount(), 'Last'),
            ],
          ),
        );
      },
    });

  R.render(R.createElement(ProgramSearchComponent, {}), document.getElementById('oie-search-component'));
});
