const SendJSONPetition = async (url, parameters) => {
	try {
        // show_spinner();
		btn_confirm_security.disabled = true;
        btn_confirm_security.innerHTML = 'Cargando ...';
        
		const response = await fetch (url, {
			method: "POST",
			body: parameters,
		});
		const data = await response.json();

		btn_confirm_security.disabled = false;
        btn_confirm_security.innerHTML = 'Confirmar';

        notifier.show(data['response']['title'], data['response']['data'], data['response']['type_response'], '', 4000);
        // hide_spinner();
		if (data['response']['type_response'] === 'danger') {
			return false
		} else if (data['response']['type_response'] === 'success') {
            $("#modal_security").modal('hide');
            window.open(data['redirect_url'])

		}

	} catch (error) {
		console.log(error);
	}
}

$(function () {
    /** BTN OPEN MODAL **/
    $('a[rel="btn_open_modal"]').on('click', function () {
        $('input[name="password1"]').val('');
        $('input[name="password2"]').val('');
        $('#modal_security').modal('show');
    });

    // SEND FORM
    $('#form_security').on('submit', async function(e) {
        e.preventDefault();
        if ($("#password1").val() !== $("#password2").val()) {
            notifier.show('Ha ocurrido un error!', 'Las contraseñas no coinciden', 'danger', '', 4000);
            $("#password1").val('');
            $("#password2").val('');
            $("#password1").focus();
        } else {
            let parameters = new FormData(this)
            await SendJSONPetition('/segutidad-de-base-de-datos/', parameters)
        }

    });
})