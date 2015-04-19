// This is a manifest file that'll be compiled into application.js, which will include all the files
// listed below.
//
// Any JavaScript/Coffee file within this directory, lib/assets/javascripts, vendor/assets/javascripts,
// or vendor/assets/javascripts of plugins, if any, can be referenced here using a relative path.
//
// It's not advisable to add code directly here, but if you do, it'll appear at the bottom of the
// compiled file.
//
// Read Sprockets README (https://github.com/sstephenson/sprockets#sprockets-directives) for details
// about supported directives.
//
//= require jquery
//= require jquery_ujs
//= require dataTables/jquery.dataTables
//= require dataTables/bootstrap/3/jquery.dataTables.bootstrap
//= require parsley
//= require turbolinks
//= require bootstrap-sprockets
//= require Chart
//= require raphael
//= require justgage
//= require flipclock.min
//= require_tree .

var eegPowerKeys = ["theta", "lowAlpha", "highAlpha", "lowBeta", "highBeta", "lowGamma", "highGamma"];

function FacebookPhoto (id, url) {
		this.id = id;
		this.url = url;
		this.eegData = [];
		this.timeLeft = 7;
		this.averages = [0, 0, 0, 0, 0, 0, 0, 0];
		this.averageAttention = 0;
		this.averageMeditation = 0;

		this.calculateAverages = function () {
			var totals = {"theta": 0, "lowAlpha": 0, "highAlpha": 0, "lowBeta": 0, "highBeta": 0, "lowGamma": 0, "highGamma": 0, "attention": 0,"meditation": 0};
			this.eegData.forEach(function(data) {
				if (typeof data.eSense != 'undefined') {
					totals['attention'] += data.eSense.attention;
					totals['meditation'] += data.eSense.meditation;
				}
				if (typeof data.eegPower != 'undefined') {
					eegPowerKeys.forEach(function(key) {
						totals[key] += data.eegPower[key];
					});
				}
			});

			var divisor = this.eegData.length;

			this.averageAttention = Math.round(totals['attention']/divisor);
			this.averageMeditation = Math.round(totals['meditation']/divisor);
			var i = 0;
			var averages = []
			eegPowerKeys.forEach(function(key) {
				averages.push(Math.round(totals[key]/divisor));
				i++;
			});
			this.averages = averages;
		};
}