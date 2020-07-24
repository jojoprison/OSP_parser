$(function () {

    var result = $('#osp_result');
    var address_region = $('#address_region');
    var address_city = $('#address_city');
    var address_street = $('#address_street');
    var address_house = $('#address_house');
    var amount_list = $('#amount_list');
    var idoc_list = $('#idoc_list');
    var ctrparty_list = $('#ctrparty_list');
    var object_list = $('#object_list');
    var debtor_list = $('#debtor_list');
    var has_document = $('#hasDocument');

    var group1 = '.e-input_isp-nodoc',
        group2 = '.e-input_isp-doc';

    $(group2).hide();
    $('.address_city').hide();
    $('.address_street').hide();
    $('.address_house').hide();
    $('.amount_list').hide();
    $('.idoc_list').hide();
    $('.ctrparty_list').hide();
    $('.object_list').hide();
    $('.debtor_list').hide();

    $(".b-chosen-select").chosen({
        disable_search_threshold: 10,
        width: "100%",
        no_results_text: 'Ничего не найдено'
    });

    has_document.change(function () {
        result.html('');
        if ($(this).prop('checked')) {
            $(group1).hide();
            $(group2).show();
            $(this).val(1);
            amount_list.val('');
            idoc_list.val('');
            ctrparty_list.val('');
            object_list.val('');
            debtor_list.val('');
            get_doc_option();
        } else {
            $(group1).show();
            $(group2).hide();
            $(this).val(2);
            showResult();
        }
    });

    address_region.change(function () {
        var code = $(this).val();
        var city = $(this).val();
        $.post('/osp/action/get_city_list/', {code: code})
            .done(function (data) {

                clear_inputs();
                result.html('');

                if (has_document.val() == 1) {
                    has_document.trigger('click');
                }

                if (data) {
                    address_street.addClass('f-disabled');
                    updateSmartList(address_street, null);
                    updateSmartList(address_city, data);
                    address_city.removeClass('f-disabled');
                    $('.address_city').show();
                }
                $('.address_street').hide();
                address_street.empty();
                $('.address_house').hide();
                address_house.empty();
                //get_doc_option();

                $.post('/osp/action/get_street_list/', {city: city})
                    .done(function (data) {
                        if (data.trim() != '') {
                            updateSmartList(address_street, data);
                            address_street.removeClass('f-disabled');
                            $('.address_street').show();
                        }

                        /*$('.address_house').hide();
                        address_house.empty();*/
                    });
            });
    });

    address_city.change(function () {
        var code = $(this).val();
        if (code != '') {
            result.html('');
            if (has_document.val() == 1) {
                amount_list.val('');
                idoc_list.val('');
                ctrparty_list.val('');
                object_list.val('');
                debtor_list.val('');
                get_doc_option();
            } else {
                address_street.val('');
                $('.address_street').hide();
                address_house.val('');
                $('.address_house').hide();
                $.post('/osp/action/get_street_list/', {code: code})
                    .done(function (data) {
                        if (typeof data == "string") {
                            data = data.replace(/(\r\n\t|\n|\r\t)/gm, "");
                        }
                        if (data) {
                            updateSmartList(address_street, data);
                            address_street.removeClass('f-disabled');
                            $('.address_house').hide();
                            address_house.empty();
                            //get_doc_option();
                        }
                        showResult();
                    });
            }
        }
    });

    address_street.change(function () {
        var code = $(this).val();
        if (code != '') {
            $.post('/osp/action/get_house_list/', {code: code})
                .done(function (data) {
                    if (data) {
                        updateList(address_house, data);
                        address_house.removeClass('f-disabled');
                        //get_doc_option();
                    }
                    showResult();
                });
        }
    });

    address_house.change(function () {
        var code = $(this).val();
        if (code != '') {
            showResult();
        }
    });

    amount_list.change(function () {
        var val = $(this).val();
        if (val != '') {
            showResult();
        }
    });

    idoc_list.change(function () {
        var val = $(this).val();
        if (val != '') {
            showResult();
        }
    });

    ctrparty_list.change(function () {
        var val = $(this).val();
        if (val != '') {
            showResult();
        }
    });

    object_list.change(function () {
        var val = $(this).val();
        if (val != '') {
            showResult();
        }
    });

    debtor_list.change(function () {
        var val = $(this).val();
        if (val != '') {
            showResult();
        }
    });

    function updateLists() {
        getList('ctrparty_list');
        getList('object_list');
        getList('amount_list');
        getList('idoc_list');
        getList('debtor_list');
    }

    function clear_inputs() {
        address_city.val('');
        address_street.val('');
        address_house.val('');
        amount_list.val('');
        idoc_list.val('');
        ctrparty_list.val('');
        object_list.val('');
        debtor_list.val('');
    }

    function getList(name) {
        $.get(
            "/osp/action/" + name,
            {
                region: address_region.val(),
                city: address_city.val(),
                kladr: result.find('.qwerty333').length ? 1 : '',
                street: address_street.val(),
                house: address_house.val(),
                amount: amount_list.val(),
                idoc: idoc_list.val(),
                ctrparty: ctrparty_list.val(),
                object: object_list.val(),
                debtor: debtor_list.val()
            },
            function (data) {
                updateList($('#' + name), data);
            }
        );
    }

    function get_doc_option() {
        $.get(
            "/osp/action/doc_option",
            {
                region: address_region.val(),
                city: address_city.val(),
                kladr: result.find('.qwerty333').length ? 1 : '',
                street: address_street.val(),
                house: address_house.val(),
                amount: amount_list.val(),
                idoc: idoc_list.val(),
                ctrparty: ctrparty_list.val(),
                object: object_list.val(),
                debtor: debtor_list.val()
            },
            function (data) {
                if (data['amount_from'] == 1)
                    $('.amount_list').show();
                else
                    $('.amount_list').hide();

                if (data['idoc_type'] == 1)
                    $('.idoc_list').show();
                else
                    $('.idoc_list').hide();

                if (data['exec_object'] == 1)
                    $('.object_list').show();
                else
                    $('.object_list').hide();

                if (data['ctrparty_class'] == 1)
                    $('.ctrparty_list').show();
                else
                    $('.ctrparty_list').hide();

                if (data['debtor_type'] == 1)
                    $('.debtor_list').show();
                else
                    $('.debtor_list').hide();

                if (data['amount_from'] == 1 && data['debtor_type'] == 1) {
                    if (has_document.val() == 2) {
                        has_document.trigger('click');
                    }
                }
            },
            "json"
        );

        updateLists();
    }

    function updateList(list, data) {
        updateSmartList(list, data);
    }

    function updateSmartList(list, data) {
        var text = has_document.val() == 1 ? 'Не указан' : 'Выбрать';
        list.empty();
        list.append('<option value="">' + text + '</option>');
        list.append(data);
        list.trigger('kladr-update');
        list.trigger("chosen:updated");
        list.removeClass('f-disabled');
    }

    function showResult() {

        if (has_document.val() == 1) {
            $.get(
                "/osp/action/result_doc",
                {
                    region: address_region.val(),
                    city: address_city.val(),
                    kladr: result.find('.qwerty333').length ? 1 : '',
                    street: address_street.val(),
                    house: address_house.val(),
                    amount: amount_list.val(),
                    idoc: idoc_list.val(),
                    ctrparty: ctrparty_list.val(),
                    object: object_list.val(),
                    debtor: debtor_list.val()
                },
                function (data) {
                    if (data) {
                        result.html(data);
                    }

                    /*if (result.find('.qwerty123').length)
                    {
                        if (!result.find('.qwerty111').length)
                        {
                            if ($('#hasDocument').prop('checked')) {
                                $(group1).show();
                                $('#hasDocument').val(2);
                                //get_doc_option();
                            }
                        }

                        updateLists();
                        showResult();
                    }*/
                }
            );
        }

        if (has_document.val() == 2) {
            $.get('/osp/action/result_ter/', {
                    region: address_region.val(),
                    city: address_city.val(),
                    kladr: result.find('.qwerty333').length ? 1 : '',
                    street: address_street.val(),
                    house: address_house.val()
                }, function (data) {
                    if (data) {
                        result.html(data);
                        if (!address_house.val() && result.find('.qwerty333').length) {
                            $('.address_house').show();
                        } else if (address_house.val() && (result.find('.qwerty333').length || result.find('.qwerty111').length)) {
                            $('.address_house').show();
                        } else if (address_house.find('option').length > 1 && !result.find('.qwerty111').length) {
                            $('.address_house').show();
                        } else $('.address_house').hide();

                        if (!address_street.val() && result.find('.qwerty111').length) {
                            $('.address_street').hide();
                        } else $('.address_street').show();

                        /*if (result.find('.qwerty111').length && address_street.val() == '')
                        {
                            updateLists();
                            $(group1).hide();
                            $('#hasDocument').val(1);
                            showResult();
                        }*/
                    }
                }
            );
        }
    }
});
