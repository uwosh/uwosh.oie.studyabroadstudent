$(document).ready(function() {
  if($('body').hasClass('template-edit') && $('body').hasClass('portaltype-oiestudyabroadprogram')) {
    var baseURL = $('body').attr('data-base-url');
    var utilURL = baseURL + '/edit-util';
    var baseWidgetSelector = '#formfield-form-widgets-';
    var baseInputSelector = '#form-widgets-';
    var util_data = {};

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
      if (load_or_overload == 'load') {
        $('select#form-widgets-replacement_costs').attr('disabled', false);
        $('select#form-widgets-paid_by').attr('disabled', true);
        handle_replacement_costs();
      } else {
        $('select#form-widgets-replacement_costs').attr('disabled', true);
        $('select#form-widgets-paid_by').attr('disabled', false);
        handle_paid_by();
      }
    }

    function handle_replacement_costs () {
      var replacement_costs = $('select#form-widgets-replacement_costs').val();
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
      if (rate_or_lump_sum == 'lump-sum') {
        enable_lump_sum_amount();
      } else {
        disable_lump_sum_amount();
      }
    }

    handle_load_or_overload();
    handle_replacement_costs();
    handle_paid_by();
    handle_rate_or_lump_sum();

    $('select#form-widgets-load_or_overload').change(handle_load_or_overload);
    $('select#form-widgets-replacement_costs').change(handle_replacement_costs);
    $('select#form-widgets-paid_by').change(handle_paid_by);
    $('select#form-widgets-rate_or_lump_sum').change(handle_rate_or_lump_sum);

    // equipment and space

    function handle_equipment_and_space() {
      var equipment_and_space_needed = $('select#form-widgets-equipment_and_space').val();
      var equipmentAndSpaceField = $('div#formfield-form-widgets-equipment_and_space_needs');
      if (equipment_and_space_needed == 'I do not need teaching space or equipment.') {
        equipmentAndSpaceField.hide();
        equipmentAndSpaceField.children('textarea').prop("required",false);
      } else {
        equipmentAndSpaceField.show();
        equipmentAndSpaceField.children('textarea').prop("required",true);
      }
    }

    handle_equipment_and_space();
    $('select#form-widgets-equipment_and_space').change(handle_equipment_and_space);

    function hideFieldsetsFromInitial(){
      if (util_data['portalState'].toLowerCase() == 'initial'){
        var editableLater = 'This fieldset becomes editable after the Initial state is completed.'
        $('#fieldset-return_flight_fieldset').replaceWith(editableLater);
        $('#fieldset-return_to_oshkosh_fieldset').replaceWith(editableLater);
        $('#fieldset-departure_flight_fieldset').replaceWith(editableLater);
        $('#fieldset-departure_from_oshkosh_fieldset').replaceWith(editableLater);
      }
    }

    $.ajax(utilURL, {
      success: function(data) {
        util_data = JSON.parse(data);
        hideFieldsetsFromInitial();
      }
    });
  }
});
