$(document).ready(function() {
  if($('.template-edit')) {
    // alert('Editing!');

    function disable_replacement_costs() {
        $('select#form-widgets-replacement_costs').attr('disabled', true);
    }
    function enable_replacement_costs() {
        $('select#form-widgets-replacement_costs').attr('disabled', false);
    }
    function disable_costs_paid_by() {
        $('select#form-widgets-paid_by').attr('disabled', true);
    }
    function enable_costs_paid_by() {
        $('select#form-widgets-paid_by').attr('disabled', false);
    }
    function disable_payment_rate_or_lump_sum() {
        $('select#form-widgets-rate_or_lump_sum').attr('disabled', true);
    }
    function enable_payment_rate_or_lump_sum() {
        $('select#form-widgets-rate_or_lump_sum').attr('disabled', false);
    }
    function disable_lump_sum_amount() {
        $('input#form-widgets-lump_sum_amount').attr('disabled', true);
    }
    function enable_lump_sum_amount() {
        $('input#form-widgets-lump_sum_amount').attr('disabled', false);
    }

    function handle_load_or_overload () {
      var load_or_overload = $('select#form-widgets-load_or_overload').val();
      // alert('Load or overload: ' + load_or_overload);
      if (load_or_overload == 'load') {
        enable_replacement_costs();
        disable_costs_paid_by();
        handle_replacement_costs();
      } else {
        disable_replacement_costs();
        enable_costs_paid_by();
        handle_paid_by();
      }
    }

    function handle_replacement_costs () {
      var replacement_costs = $('select#form-widgets-replacement_costs').val();
      // alert('Replacement costs: ' + replacement_costs);
      if (replacement_costs == 'due') {
        enable_payment_rate_or_lump_sum();
        handle_rate_or_lump_sum();
      } else {
        disable_payment_rate_or_lump_sum();
        disable_lump_sum_amount();
      }
    }

    function handle_paid_by() {
      var paid_by = $('select#form-widgets-paid_by').val();
      // alert('Paid by: ' + paid_by);
      if (paid_by == 'students') {
        enable_payment_rate_or_lump_sum();
        handle_rate_or_lump_sum();
      } else {
        disable_payment_rate_or_lump_sum();
        disable_lump_sum_amount();
      }
    }

    function handle_rate_or_lump_sum () {
      var rate_or_lump_sum = $('select#form-widgets-rate_or_lump_sum').val();
      // alert('Rate or lump sum: ' + rate_or_lump_sum);
      if (rate_or_lump_sum == 'lump-sum') {
        enable_lump_sum_amount();
      } else {
        disable_lump_sum_amount();
      }
    }

    // alert(jQuery.fn.jquery);
    handle_load_or_overload();
    handle_replacement_costs();
    handle_paid_by();
    handle_rate_or_lump_sum();

    $('select#form-widgets-load_or_overload').change(handle_load_or_overload);
    $('select#form-widgets-replacement_costs').change(handle_replacement_costs);
    $('select#form-widgets-paid_by').change(handle_paid_by);
    $('select#form-widgets-rate_or_lump_sum').change(handle_rate_or_lump_sum);
  }
});
