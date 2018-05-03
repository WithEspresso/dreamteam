var app = new Vue({
  el: '#app',
  data: {
    // periodTotalHours: 0,
    weeks: [{
      totalHours: 0,
      // totalDeductions: 0,
      // totalVacation: 0,
      // totalPersonal: 0,
      // totalUnpaid: 0,
      days: [{
        // date: "2016-01-02",
        date: "",
        hours: 0,
        // in: "08:30",
        // out: "17:00",
        // deductions: .5,
        // vacation: 0,
        // personal: 0,
        // unpaid: 0,
        dailyTotal: 0
      }, {
        // date: "2016-01-02",
        date: "",
        hours: 0,
        // in: "08:30",
        // out: "17:00",
        // deductions: .5,
        // vacation: 0,
        // personal: 0,
        // unpaid: 0,
        dailyTotal: 1
      }, {
        // date: "2016-01-03",
        date: "",
        hours: 0,
        // in: "08:30",
        // out: "17:00",
        // deductions: .5,
        // vacation: 0,
        // personal: 0,
        // unpaid: 0,
        dailyTotal: 2
      }, {
        // date: "2016-01-04",
        date: "",
        hours: 0,
        // in: "08:30",
        // out: "17:00",
        // deductions: .5,
        // vacation: 0,
        // personal: 0,
        // unpaid: 0,
        dailyTotal: 3
      }, {
        // date: "2016-01-05",
        date: "",
        hours: 0,
        // in: "08:30",
        // out: "17:00",
        // deductions: .5,
        // vacation: 0,
        // personal: 0,
        // unpaid: 0,
        dailyTotal: 4
      }, {
        date: "",
        hours: 0,
        // in: "",
        // out: "",
        // deductions: 0,
        // vacation: 0,
        // personal: 0,
        // unpaid: 0,
        dailyTotal: 0
      }, {
        date: "",
        hours: 0,
        // in: "",
        // out: "",
        // deductions: 0,
        // vacation: 0,
        // personal: 0,
        // unpaid: 0,
        dailyTotal: 0
      }]
    }]
  },
  methods: {
    dailyTotal: function(day) {
      // var start = moment(day.date + " " + day.in);
      // var end = moment(day.date + " " + day.out);
      // var ded = day.deductions;
      // var vacation = day.vacation;
      // var personal = day.personal;
      // var unpaid = day.unpaid;
      //
      // if( day.date == "" || day.in== "" || day.out == "")
      // {
      //   day.deductions = 0;
      //     return 0;
      // }
      //
      // var dailyTotal = (end.diff(start, 'minutes') / 60) - ded;
      //
      // dailyTotal += parseFloat(vacation);
      //
      // dailyTotal += parseFloat(personal);
      //
      // dailyTotal += parseFloat(unpaid);
      //
      // day.dailyTotal = dailyTotal.toFixed(2);
      //
      // return dailyTotal.toFixed(2);

      return 15;
    }

    // calcWeekDeductions: function(week) {
    //   var weekDeductions = 0;
    //
    //   for (var i = 0; i < week.days.length; i++) {
    //     weekDeductions += parseFloat(week.days[i].deductions);
    //   }
    //
    //   week.totalDeductions = weekDeductions;
    //
    //   return weekDeductions;
    // },
    //
    // calcWeekHours: function(week) {
    //   var weekHours = 0;
    //
    //   for (var i = 0; i < week.days.length; i++) {
    //     weekHours += parseFloat(week.days[i].dailyTotal);
    //   }
    //
    //   week.totalHours = weekHours;
    //
    //   return weekHours.toFixed(2);
    // },
    //
    // periodTotalHours: function() {
    //   var weekTotal = 0;
    //
    //   console.log(this.weeks.length)
    //   for (var i = 0; i < weeks.length; i++) {
    //
    //   }
    //
    //   return weekTotal;
    // }
  }
})


/***********************************************
* Other functions
***********************************************/
$('#submit').click(function() {
  swal({
    title: "Are you sure?",
    text: "You will be unable to edit the timesheet once it has been submitted.",
    type: "warning",
    showCancelButton: true,
    confirmButtonColor: "#5cb85c",
    confirmButtonText: "Yes, submit my timesheet.",
    cancelButtonText: "No, cancel.",
    closeOnConfirm: false,
    closeOnCancel: false
  }, function(isConfirm) {
    if (isConfirm) {
      swal("Submitted!", "Your timesheet has been successfully submitted", "success");
    } else {
      swal("Submission Cancelled", "Submission cancelled. You can still edit your timesheet!", "error");
    }
  });
});

$('#save').click(function() {
  swal("Timesheet Saved!","", "success");
});

$('#delete').click(function() {
  swal({
    title: "Are you sure?",
    text: "Are you sure you want to delete this timesheet?",
    type: "warning",
    showCancelButton: true,
    confirmButtonColor: "#d9534f",
    confirmButtonText: "Yes, delete this timesheet.",
    cancelButtonText: "No, cancel.",
    closeOnConfirm: false,
    closeOnCancel: false
  }, function(isConfirm) {
    if (isConfirm) {
      swal("Deleted!", "Your timesheet has been successfully deleted!", "success");
    } else {
      swal("Deletion Cancelled", "Your timesheet has not been deleted", "error");
    }
  });
});