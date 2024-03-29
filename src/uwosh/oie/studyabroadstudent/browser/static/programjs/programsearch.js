

require([
  '++plone++uwosh.oie.studyabroadstudent/libs/react/react.min',
], function(R) {
  const D = R.DOM;
  const ProgramSearchComponent = R.createClass({

    getInitialState: function(){
      const defaultFilters = {
        type: false,
        title: null,
        calendarYear: false,
        countries: false,
        term: false,
        college: false,
        leader: false,
      };
      const noMatchingPrograms = D.div(
        {},
        [ D.span({}, ['No Matching Programs'])]
      );
      return {
        noMatchingPrograms,
        defaultFilters,
        filters: {...defaultFilters},
        currentPage: 1,
        perPage: 12,
        titles: [],
        years: [],
        terms: [],
        leaders: [],
        colleges: [],
        types: [],
        countries: [],
        programs: [],
        activePrograms: [],
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

    componentDidMount: async function(){
      const portalUrl = document.body.getAttribute('data-portal-url');
      const programDataUrl = `${portalUrl}/@@discoverable-program-data`
      const response = await fetch(programDataUrl)
      const programsJson = await response.json()
      const programs = Array.from(programsJson)
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
      this.setState({
        programs,
        activePrograms: [...programs],
        titles,
        years,
        terms,
        leaders,
        colleges,
        types,
        countries,
        portalUrl,
      });
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
            .filter(value => !this.state.nullValues.includes(value))
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
          this.getOptions(this.state.countries, 'Program Country')
        );

        const typeField = D.select(
          {
            className: 'form-control oie-search-field',
            name: 'type',
            onChange: this.handler.bind(this),
          },
          this.getOptions(this.state.types, 'Program Type'),
        );

        const collegeField = D.select(
          {
            className: 'form-control oie-search-field',
            name: 'college',
            onChange: this.handler.bind(this),
          },
          this.getOptions(this.state.colleges, 'Program College'),
        );

        const termField = D.select(
          {
            className: 'form-control oie-search-field',
            name: 'term',
            onChange: this.handler.bind(this),
          },
          this.getOptions(this.state.terms, 'Program Term')
        );

        const yearField = D.select(
          {
            className: 'form-control oie-search-field',
            name: 'calendarYear',
            onChange: this.handler.bind(this),
          },
          this.getOptions(this.state.years, 'Program Year')
        );

        const leaderField = D.select(
          {
            className: 'form-control oie-search-field',
            name: 'leader',
            onChange: this.handler.bind(this),
          },
          this.getOptions(this.state.leaders, 'Program Leader')
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

      currentPageWillBeOutOfBounds: function(activePrograms){
        return (this.state.currentPage - 1) * this.state.perPage >= activePrograms.length;
      },

      handler: function(event){
        event.preventDefault();
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
        if(this.currentPageWillBeOutOfBounds(activePrograms)){
          this.setState({currentPage: 1});
        }
      },

      getForm: function() {
        return document.getElementById('oie-search-form');
      },

      resetSearchFields: function(event){
        event.preventDefault();
        this.getForm().reset();
        const filters = {...this.state.defaultFilters};
        this.setState({
          filters,
          activePrograms: this.getFilteredResults(filters),
        });
      },

      filtersMatch: function(filterName, filterValue, program){
        const actualValue = program[filterName];
        if(
          this.state.nullValues.includes(filterValue) ||
          this.state.nullValues.includes(actualValue)
          ){
          return true;
        }
        switch(typeof filterValue){
          case 'boolean':
            return filterValue === false || this.state.trueValues.includes(actualValue); //this might be a mistake?
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
            this.state.programs,
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
          .map((program,index) => {
            const imgSrc = program.image || '/oie/++theme++oie-study-abroad-theme/img/logo.png';
            const title = D.div(
              {className: `search-program-title search-program-title-${index + 1}`},
              D.a({href: program.url}, program.title),
            );
            const programImage = D.img({
              className: `search-program-image search-program-image-${index + 1} focuspoint`,
              alt: '',
              src: imgSrc,
            });
            const description = D.p(
              {className: `search-program-description search-program-description-${index + 1}`},
              program.description,
            );
            const more = D.a(
              { className: `search-program-link search-program-link-${index + 1}`, href: program.url },
            'More...',
            );
            return D.div(
              { className: 'search-program-view' },
              [
                title,
                programImage,
                description,
                more,
              ],
            );
          });
        return D.div(
          { className: 'program-group col-xs-12' },
          views,
        );
      },

      renderPrograms: function(){
        const activeProgramCount = this.getActiveProgramCount();
        let programsFoundText = '';
        switch(activeProgramCount){
          case 0:
            return this.state.noMatchingPrograms;
          case 1:
            programsFoundText = '1 program found';
            break;
          default:
            programsFoundText = `${activeProgramCount} programs found`;
            break;
        }
        return D.div(
          { className: 'program-listing' },
          [
             D.span(
              { className: 'oie-search-counter col-xs-12' },
              programsFoundText,
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
          this.setState({ currentPage: page });
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

  R.render(
    R.createElement(
      ProgramSearchComponent,
      {},
    ),
    document.getElementById('oie-search-component'),
  );
});
