var app = angular.module("IronManApp", ['nvd3']);

app.factory('AthleteService', function ($http) {
    var eventData = {};
    var promise;
    eventData.getEvent = function (event) {
        if (!promise) {
            promise = $http.get('/athletes', event)
                .error(function () { // this is optional
                    promise = false;
                });
        }
        return promise;
    };
    return eventData;
});


app.controller("TimeDistributionController", function ($scope, $http, AthleteService) {

    AthleteService.getEvent().success(function (response) {
        $scope.chartLoaded = true;

        var counts = {};
        response.athletes.forEach(function (athlete) {
            if (counts[athlete.finish_time - (athlete.finish_time % 100)] == undefined)
                counts[athlete.finish_time - (athlete.finish_time % 100)] = 0;
            else
                counts[athlete.finish_time - (athlete.finish_time % 100)]++;
        });

        var data = [];
        for (var key in counts)
            data.push({label: key, value: counts[key], color: 'gray'})


        $scope.data = [
            {
                key: "Distribution",
                values: data
            }
        ]
    });
    $scope.options = {
        chart: {
            showControls: false,
            type: 'multiBarChart',
            height: 450,
            margin: {
                top: 20,
                right: 20,
                bottom: 50,
                left: 55
            },
            x: function (d) {
                return d.label;
            },
            y: function (d) {
                return d.value + (1e-10);
            },
            showValues: true,
            valueFormat: function (d) {
                return d3.format('d')(d);
            },
            duration: 500,
            xAxis: {
                axisLabel: 'Overall time (seconds)',
                rotateLabels: -35
            },
            yAxis: {
                axisLabel: 'Number of people',
                axisLabelDistance: -10
            }
        }
    };
});

app.controller("BikeVsSwimController", function ($scope, AthleteService) {

    AthleteService.getEvent().success(function (response) {
        $scope.chartLoaded = true;

        var data = [];
        response.athletes.forEach(function (athlete) {
            data.push(
                {
                    x: athlete.bike_time,
                    y: athlete.swim_time,
                    shape: "circle",
                    size: 0.5
                })
        });

        $scope.data = [
            {
                key: "Distribution",
                color: "green",
                values: data
            }
        ]
    });

    $scope.options = {
        chart: {
            type: 'scatterChart',
            height: 350,
            color: d3.scale.category10().range(),
            scatter: {
                onlyCircles: false
            },
            showDistX: true,
            showDistY: true,
            tooltipContent: function (key) {
                return '<h3>' + key + '</h3>';
            },
            duration: 350,
            xAxis: {
                axisLabel: 'X Axis',
                tickFormat: function (d) {
                    return d3.format('.02f')(d);
                }
            },
            yAxis: {
                axisLabel: 'Y Axis',
                tickFormat: function (d) {
                    return d3.format('.02f')(d);
                },
                axisLabelDistance: -5
            },
            zoom: {
                //NOTE: All attributes below are optional
                enabled: false,
                scaleExtent: [1, 10],
                useFixedDomain: false,
                useNiceScale: false,
                horizontalOff: false,
                verticalOff: false,
                unzoomEventType: 'dblclick.zoom'
            }
        }
    };
});

app.controller("SwimVsRunController", function ($scope, AthleteService) {

    AthleteService.getEvent().success(function (response) {
        $scope.chartLoaded = true;

        var data = [];
        response.athletes.forEach(function (athlete) {
            data.push(
                {
                    x: athlete.run_time,
                    y: athlete.swim_time,
                    shape: "circle",
                    size: 0.5
                })
        });

        $scope.data = [
            {
                key: "Distribution",
                color: "blue",
                values: data
            }
        ]
    });

    $scope.options = {
        chart: {
            type: 'scatterChart',
            height: 350,
            color: d3.scale.category10().range(),
            scatter: {
                onlyCircles: false
            },
            showDistX: true,
            showDistY: true,
            tooltipContent: function (key) {
                return '<h3>' + key + '</h3>';
            },
            duration: 350,
            xAxis: {
                axisLabel: 'X Axis',
                tickFormat: function (d) {
                    return d3.format('.02f')(d);
                }
            },
            yAxis: {
                axisLabel: 'Y Axis',
                tickFormat: function (d) {
                    return d3.format('.02f')(d);
                },
                axisLabelDistance: -5
            },
            zoom: {
                //NOTE: All attributes below are optional
                enabled: false,
                scaleExtent: [1, 10],
                useFixedDomain: false,
                useNiceScale: false,
                horizontalOff: false,
                verticalOff: false,
                unzoomEventType: 'dblclick.zoom'
            }
        }
    };
});

app.controller("BikeVsRunController", function ($scope, $http, AthleteService) {

    AthleteService.getEvent().success(function (response) {
        $scope.chartLoaded = true;

        var data = [];
        response.athletes.forEach(function (athlete) {
            data.push(
                {
                    x: athlete.bike_time,
                    y: athlete.run_time,
                    shape: "circle",
                    size: 0.5
                })
        });

        $scope.data = [
            {
                key: "Distribution",
                color: "red",
                values: data
            }
        ]
    });
    $scope.options = {
        chart: {
            type: 'scatterChart',
            height: 350,
            color: d3.scale.category10().range(),
            scatter: {
                onlyCircles: false
            },
            showDistX: true,
            showDistY: true,
            tooltipContent: function (key) {
                return '<h3>' + key + '</h3>';
            },
            duration: 350,
            xAxis: {
                axisLabel: 'X Axis',
                tickFormat: function (d) {
                    return d3.format('.02f')(d);
                }
            },
            yAxis: {
                axisLabel: 'Y Axis',
                tickFormat: function (d) {
                    return d3.format('.02f')(d);
                },
                axisLabelDistance: -5
            },
            zoom: {
                //NOTE: All attributes below are optional
                enabled: false,
                scaleExtent: [1, 10],
                useFixedDomain: false,
                useNiceScale: false,
                horizontalOff: false,
                verticalOff: false,
                unzoomEventType: 'dblclick.zoom'
            }
        }
    };
});


app.controller('SwimRunBikeConnectionsController', function ($scope, AthleteService) {

    AthleteService.getEvent().success(function (response) {
        $scope.dataBest = response.athletes.slice(0, 99);
        $scope.dataWorst = response.athletes.slice(response.athletes.length - 100, response.athletes.length)

        $scope.chartLoaded = true;
    });

    $scope.options = {
        chart: {
            type: 'parallelCoordinates',
            height: 450,
            // width: 600,
            margin: {
                top: 30,
                right: 10,
                bottom: 10,
                left: 10
            },
            dimensions: [
                "finish_time",
                "run_time",
                "swim_time",
                "bike_time",
                "age"
            ]
        }
    };


});

app.controller('AttendanceByCountryController', function ($scope, AthleteService) {

    AthleteService.getEvent().success(function (response) {

        var counts = {};

        response.athletes.forEach(function (athlete) {
            if (counts[athlete.country] == undefined) {
                counts[athlete.country] = 1;
            } else {
                counts[athlete.country]++;
            }
        });

        var data = [];

        for (var key in counts) {

            data.push({
                label: key,
                value: counts[key]
            })
        }

        $scope.data = [
            {
                key: 'Series1',
                color: 'blue',
                values: _.sortBy(data, 'value').reverse()
            }
        ];
        $scope.chartLoaded = true;

    });

    $scope.options = {
        chart: {
            type: 'discreteBarChart',
            height: 450,
            x: function (d) {
                return d.label;
            },
            y: function (d) {
                return d.value;
            },
            showControls: false,
            showValues: false,
            duration: 500,
            xAxis: {
                axisLabel: 'Country of origin',
                rotateLabels: -90
            },
            yAxis: {
                axisLabel: 'Number of people',
                tickFormat: function (d) {
                    return d3.format('d')(d);
                }
            }
        }
    };


});

app.controller("AttendanceByAgeController", function ($scope, $http, AthleteService) {

    AthleteService.getEvent().success(function (response) {

        var counts = {};

        response.athletes.forEach(function (athlete) {
            if (counts[athlete.age] == undefined) {
                counts[athlete.age] = 1;
            } else {
                counts[athlete.age]++;
            }
        });

        var data = [];

        for (var key in counts) {

            data.push({
                label: key,
                value: counts[key]
            })
        }

        $scope.data = [
            {
                key: 'Series1',
                color: '#1ab394',
                values: _.sortBy(data, 'label')
            }
        ];

        $scope.chartLoaded = true;
    });

    $scope.options = {
        chart: {
            showControls: false,
            type: 'multiBarChart',
            height: 450,
            margin: {
                top: 20,
                right: 20,
                bottom: 50,
                left: 55
            },
            x: function (d) {
                return d.label;
            },
            y: function (d) {
                return d.value;
            },
            showValues: true,
            valueFormat: function (d) {
                return d3.format('d')(d);
            },
            duration: 500,
            xAxis: {
                axisLabel: 'Age',
                rotateLabels: -35
            },
            yAxis: {
                axisLabel: 'Number of attendees',
                axisLabelDistance: -10
            }
        }
    };
});


app.controller('TimeTablesController', function ($scope, AthleteService) {

    AthleteService.getEvent().success(function (response) {

        $scope.topOverall = _.sortBy(response.athletes, 'finish_time')
            .slice(response.athletes.length - 5, response.athletes.length);

        $scope.topSwimmers = _.sortBy(response.athletes, 'swim_time')
            .slice(response.athletes.length - 5, response.athletes.length);

        $scope.topBikers = _.sortBy(response.athletes, 'bike_time')
            .slice(response.athletes.length - 5, response.athletes.length);

        $scope.topRunners = _.sortBy(response.athletes, 'run_time')
            .slice(response.athletes.length - 5, response.athletes.length);

        $scope.chartLoaded = true;

    });
});

app.directive('myOnKeyDownCall', function () {
    return function ($scope, element) {
        element.bind("keyup", function (event) {
            var val = element.val();
            if (val.length > 2) {
                $scope.search(val);
            }
        });
    };
});

app.directive('loadingSpinner', function () {
    return {
        template: '<div class="row" style="text-align: center;"><div class="span12"><i  ng-hide="chartLoaded" class="text-center fa fa-circle-o-notch fa-spin" style="font-size:24px"></i></div></div>',
    }
});


app.controller('SearchController', function ($scope, $http) {

    $scope.search = function () {
        $http({
            method: 'GET',
            params: {q: $scope.searchText},
            url: 'http://ironman.graflr.co/search'
        }).success(function (data) {
            $scope.results = data.hits;
        })
    }
});

