/**
 * Created by Steven
 */
$(document).ready(function () {
    var app = angular.module('CrontabModule', []);

    function CronItem(exp) {
        this.type = 'every';
        this.n = '';
        this.each = '';
        this.list = [];
        this.labelList = [];
    }

    CronItem.prototype = {
        isFromZero: true,
        range: [],
        appendSelected: function () {
            if (this.each === '') {
                return;
            }
            var index = $.inArray(this.each, this.labelList);
            if (index < 0) {
                this.labelList.push(this.each);
                var di = $.inArray((/^\d+$/.test(this.each)) ? +this.each : this.each, this.range);
                this.list.push(this.isFromZero ? di : (di + 1));
            }
            this.each = '';
        },
        removeSelected: function (txt) {
            var that = this;
            var index = $.inArray(txt, this.labelList);
            this.labelList = $.grep(this.labelList, function (value) {
                return value != txt;
            });
            this.list = $.grep(this.list, function (value) {
                return value != that.list[index];
            });
            if (this.list.length == 0) {
                this.each = '';
            }
        },
        getExpression: function () {
            var tmp = '*';
            if (this.type === 'every') {
                tmp = '*';
            } else if (this.type === 'everyN') {
                if (this.n.length > 0) {
                    tmp = '*/' + this.n;
                }
            } else {
                if (this.list && this.list.length > 0) {
                    tmp = this.list.join(',');
                }
            }
            return tmp;
        },
        decodeExpression: function (txt) {
            var that = this;
            this.each = '';
            if (txt === undefined || txt === null || txt === '*') {
                this.type = 'every';
                this.n = '';
                this.list = [];
                this.labelList = [];
            } else if (txt.indexOf('*/') > -1) {
                this.type = 'everyN';
                this.n = txt.substr(txt.indexOf('*/') + 2);
                this.list = [];
                this.labelList = [];
            } else if (txt.indexOf(',') > -1 || /^\d+$/.test(txt)) {
                this.type = 'each';
                this.n = '';
                this.list = txt.split(',');
                $.each(this.list, function (i, v) {
                    that.labelList.push(that.isFromZero ? that.range[v] : that.range[v - 1]);
                });
            }
        }
    };
    function MinCronItem(exp) {
        CronItem.call(this, exp);
        this.decodeExpression(exp);
    }

    MinCronItem.prototype = {
        range: range(0, 59)
    };

    function HourCronItem(exp) {
        CronItem.call(this);
        this.decodeExpression(exp);
    }

    HourCronItem.prototype = {
        range: range(0, 23)
    };

    function DayMCronItem(exp) {
        CronItem.call(this, exp);
        this.decodeExpression(exp);
    }

    DayMCronItem.prototype = {
        isFromZero: false,
        range: range(1, 31)
    };

    function MonthCronItem(exp) {
        CronItem.call(this);
        this.decodeExpression(exp);
    }

    MonthCronItem.prototype = {
        isFromZero: false,
        range: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    };

    function DayWCronItem(exp) {
        CronItem.call(this);
        this.decodeExpression(exp);
    }

    DayWCronItem.prototype = {
        range: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    };

    inheritPrototype(MinCronItem, CronItem);
    inheritPrototype(HourCronItem, CronItem);
    inheritPrototype(DayMCronItem, CronItem);
    inheritPrototype(MonthCronItem, CronItem);
    inheritPrototype(DayWCronItem, CronItem);

    app.controller('CrontabController', ['$scope', function ($scope) {
        $scope.cron = {};
        $scope.cron.reset = resetCron;
        resetCron();

        function resetCron() {
            $scope.cron.min = new MinCronItem('0');
            $scope.cron.hour = new HourCronItem();
            $scope.cron.dayM = new DayMCronItem();
            $scope.cron.month = new MonthCronItem();
            $scope.cron.dayW = new DayWCronItem();
        }
    }]);
    angular.bootstrap(document, ['CrontabModule']);

    function inheritPrototype(subClass, baseClass) {
        for (var prop in baseClass.prototype) {
            if (typeof(subClass.prototype[prop]) === 'undefined') {
                subClass.prototype[prop] = baseClass.prototype[prop];
            }
        }
        subClass.prototype.constructor = subClass;
    }

    function range(min, max) {
        var input = [];
        for (var i = min; i <= max; i++) {
            input.push(i);
        }
        return input;
    }
});