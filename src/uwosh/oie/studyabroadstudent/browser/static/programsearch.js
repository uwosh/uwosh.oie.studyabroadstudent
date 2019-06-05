require([
  '++plone++uwosh.oie.studyabroadstudent/libs/react/react.min',
], function(R) {
  var D = R.DOM;

  var ProgramSearchComponent = R.createClass({
      getInitialState: function(){
        var el = document.getElementById('oie-search');
        var encoded = el.getAttribute('oie-program-data');
        var programs = JSON.parse(window.atob(encoded));
        var unfilteredPrograms = programs.slice()
        var types = [];
        // Iterate and get list of types
        var years = [];
        // Iterate and get/sort list of years
        return {
          programs: programs,
          count: programs.length,
          activePrograms: unfilteredPrograms,
          types: types,
          filters: {
            type: false,
            title: false,
            year: false
          },
          markers: [],
          page: 1,
          perPage: 12
        };
      },

      getDefaultProps: function(){
        var portal_url = document.body.getAttribute('data-portal-url')
        return {
          portal_url: portal_url
        };
      },

      componentDidMount: function(){

      },

      render: function(){
        this.filter();
        var programsearch = D.div({}, [
          D.div({
            id: 'oie-search',
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
          className: 'oie-search-field',
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
          className: 'oie-search-field',
          name: 'types',
          onChange: this.handler
        }, types);
        searchFields.push(typeField);

        // TODO calendar year field

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
        // TODO add Clear button to call this
        // set each field back to default value
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
            var actualValues = actualValue;
            if (!Array.isArray(actualValue)) {
              actualValues = [actualValue];
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
          return;
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
            var attributes = {
            }
            var programImage = D.div(attributes,
              [D.img({
                className: 'search-program-image focuspoint',
                alt: '',
                src: program.image
              })]);
            fields.push(programImage);
          }
          fields.push(D.a({
            className: 'search-program-title',
            href: program.url
          }, program.title));
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
