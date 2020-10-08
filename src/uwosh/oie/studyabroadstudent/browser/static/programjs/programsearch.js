require([
  '++plone++uwosh.oie.studyabroadstudent/libs/react/react.min',
], function(R) {
  var D = R.DOM;

  var ProgramSearchComponent = R.createClass({
      getInitialState: function(){
        var el = document.getElementById('oie-search');
        var program_data = el.getAttribute('oie-program-data');
        var programs = JSON.parse(program_data);
        var unfilteredPrograms = programs.slice();
        var types = [];
        var years = [];
        var countries = [];
        for (var i=0;i<programs.length;i++) {
          var program = programs[i];
          if (types.indexOf(program.type) == -1) {
            types.push(program.type);
          }
          if (years.indexOf(program.calendarYear) == -1) {
            years.push(program.calendarYear);
          }
          for (var j=0;j<program.countries.length;j++){
            if (countries.indexOf(program.countries[j]) == -1) {
              countries.push(program.countries[j]);
            }
          }
        }
        return {
          programs: programs,
          count: programs.length,
          activePrograms: unfilteredPrograms,
          types: types,
          countries: countries,
          years: years,
          filters: Object.assign({},this.props.defaultFilters),
          markers: [],
          page: 1,
          perPage: 12
        };
      },

      getDefaultProps: function(){
        var portal_url = document.body.getAttribute('data-portal-url')
        var defaultFilters = {
          type: false,
          title: false,
          calendarYear: false,
          countries: false
        }
        return {
          portal_url: portal_url,
          defaultFilters: defaultFilters
        };
      },

      componentDidMount: function(){

      },

      render: function(){
        this.filter();
        var programsearch = D.div({}, [
          D.form({
            id: 'oie-search-form',
            'aria-hidden': 'true'
          },
            this.renderSearchFields()),
          this.renderPrograms()
        ]);

        return programsearch;
      },

      renderSearchFields: function(){
        var searchFields = [];

        var titleField = D.input({
          className: 'form-control oie-search-field',
          type: 'text',
          name: 'title',
          placeholder: 'Program Name/Title',
          onChange: this.handler
        });
        searchFields.push(titleField);

        var types = [D.option({
          selected: true,
          value: 'n/a'
        }, '--Select a Program Type--')];
        for (var i=0;i<this.state.types.length;i++) {
          types.push(D.option({
            value: this.state.types[i][0]
          }, this.state.types[i][1]));
        }

        var typeField = D.select({
          className: 'form-control oie-search-field',
          name: 'type',
          onChange: this.handler
        }, types);
        searchFields.push(typeField);

        var years = [D.option({
          selected: true,
          value: 'n/a'
        }, '--Select a Program Year--')];
        for (var i=0;i<this.state.years.length;i++) {
          years.push(D.option({
            value: this.state.years[i]
          }, this.state.years[i]));
        }

        var yearField = D.select({
          className: 'form-control oie-search-field',
          name: 'calendarYear',
          onChange: this.handler
        }, years);
        searchFields.push(yearField);

        var countries = [D.option({
          selected: true,
          value: 'n/a'
        }, '--Select a Country--')];
        for (var i=0;i<this.state.countries.length;i++) {
          countries.push(D.option({
            value: this.state.countries[i]
          }, this.state.countries[i]));
        }

        var countryField = D.select({
          className: 'form-control oie-search-field',
          name: 'countries',
          onChange: this.handler
        }, countries);
        searchFields.push(countryField);


        var clearButton = D.button({
          className: 'btn btn-primary clear-button',
          onClick: this.resetSearchFields
        }, 'Clear');
        searchFields.push(clearButton);

        return searchFields;
      },

      handler: function(event){
        if (event.target.type == 'checkbox'){
          this.state.filters[event.target.name] = event.target.checked;
        } else {
          this.state.filters[event.target.name] = event.target.value;
        }
        this.setState({
          filters: this.state.filters
        });
      },

      resetSearchFields: function(event){
        event.preventDefault();
        form = document.getElementById('oie-search-form');
        form.reset();
        this.setState({
          filters: Object.assign({}, this.props.defaultFilters)
        });
      },

      filter: function(){
        results = [];
        var that = this;
        var match = function(key, program) {
          var filterValue = that.state.filters[key];
          var actualValue = program[key];
          if (actualValue == null) {
            return false;
          }
          if (typeof(filterValue) === 'boolean') {
            if (filterValue == false) {
              return true;
            }
            var trueValues = [
              true,
              'true',
              'True',
              'Yes',
              'yes',
              'Y',
              'y'
            ];
            if (trueValues.indexOf(actualValue) >= 0) {
              return true;
            }
          } else if (typeof(filterValue) === 'string') {
            filterValue = filterValue.toLowerCase().trim();
            if (!Array.isArray(actualValue)) {
              var actualValues = [actualValue];
            } else {
              var actualValues = actualValue;
            }
            for (var i=0;i<actualValues.length;i++) {
              actualValue = actualValues[i].toLowerCase().trim();
              if (actualValue.indexOf(filterValue) >= 0) {
                return true;
              }
            }
          }
          return false;
        }

        var nullValues = [
          null,
          'null',
          'N/A',
          'n/a',
          'na',
          ''
        ];

        for (var idx=0; idx<this.state.programs.length; idx++) {
          program = this.state.programs[idx];
          var match_all = true;
          var filterKeys = Object.keys(this.state.filters);
          for (var fIdx=0;fIdx<filterKeys.length;fIdx++){
            key = filterKeys[fIdx]
            if (nullValues.indexOf(this.state.filters[key]) >= 0) {
              continue;
            }
            if (!match(key,program)) {
              match_all = false;
              break;
            }
          }
          if (match_all) {
            results.push(idx);
          }
        }
        this.state.activePrograms = results;
        this.state.count = results.length;
      },

      renderPrograms: function(){
        if (!this.state.count) {
          noResults = D.div({}, [
            D.span({}, [
              'No Matching Programs'
            ])
          ])
          return noResults;
        }

        var views = [];

        var counter = D.span({
          className: 'oie-search-counter col-xs-12'
        }, this.state.count + ' programs(s) found');

        var offset = this.state.perPage * (this.state.page - 1);
        for (var i=offset;i<offset+this.state.perPage;i++) {
          if(i>=this.state.count){
            break;
          }
          var programIndex = this.state.activePrograms[i];
          var program = this.state.programs[programIndex];
          var fields = [];
          if (program.image) {
            var imgSrc = program.image
          } else {
            var imgSrc = '/oie/++theme++oie-study-abroad-theme/img/logo.png';
         }
         var title = D.div({className: 'search-program-title'}, D.a({
               href: program.url
            }, program.title));
         fields.push(title);
         var programImage = D.div({className: 'image-container'},
           [D.img({
              className: 'search-program-image focuspoint',
              alt: '',
              src: imgSrc
            })]);
          fields.push(programImage);
          fields.push(D.p({
            className: 'search-program-description'
          }, program.description));
          fields.push(D.a({
            className: 'search-program-link',
            href: program.url
          }, 'More...'));
          views.push(D.div({
            className: 'search-program-view col-lg-2 col-md-3 col-sm-4'
          }, D.div({
              className: 'program-margin'
            }, fields)));
        }

        programsView = D.div({
          className: 'program-group col-xs-12'
        }, views);

        return D.div({
          className: 'program-listing'
        }, [
          counter,
          programsView,
          this.renderPaging()]
        );
        return programsView;
      },

      renderPaging: function() {
        var pages = [];
        var that = this;
        var pageCount = Math.ceil(this.state.count / this.state.perPage);
        var pageClick = function(event) {
          event.preventDefault();
          var page = parseInt(event.target.target)
          if (page > 0 && page <= pageCount){
            that.setState({
              page: parseInt(event.target.target)
            });
          }
        }
        var renderPage = function(number, label) {
          var liAttributes = {
            className: 'page-item'
          }
          if (label == undefined) {
            label = number;
          }
          if (number == that.state.page) {
            liAttributes.className = 'page-item current';
          } else if (number < 1 || number > pageCount) {
            liAttributes.className = 'page-item disabled'
          }
          var link = D.a({
            onClick: pageClick,
            href: number,
            target: number,
            className: 'page-link'
          }, label)
          var page = D.li(liAttributes, link);
          return page;
        }
        pages.push(renderPage(1, 'First'));
        pages.push(renderPage(this.state.page-1, 'Prev'));
        if (this.state.page > 1 ) {
          if (this.state.page > 2) {
            pages.push(renderPage(this.state.page-2));
          }
          pages.push(renderPage(this.state.page-1));
        }
        pages.push(renderPage(this.state.page));
        var nextPage = this.state.page+1;
        while (pages.length < 10 && nextPage<=pageCount) {
          pages.push(renderPage(nextPage));
          nextPage++;
        }
        pages.push(renderPage(this.state.page+1, 'Next'));
        pages.push(renderPage(pageCount, 'Last'));
        return D.div({
          className: 'oie-paging'
        }, D.ul({
            className: 'pagination'
          }, pages));
      },

    });

  R.render(R.createElement(ProgramSearchComponent, {}), document.getElementById('oie-search-component'));
});
