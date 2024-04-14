const SendJSONPetition = async (url, parameters) => {
	try {
		btn_confirm_security.disabled = true;
        file_input.disabled = true;
        btn_confirm_security.innerHTML = 'Cargando ...'
		const response = await fetch (url, {
			method: "POST",
			body: parameters,
		});
		const data = await response.json();
		btn_confirm_security.disabled = false;
        btn_confirm_security.innerHTML = 'Confirmar'
        file_input.disabled = false;

        notifier.show(data['response']['title'], data['response']['data'], data['response']['type_response'], '', 4000);

		if (data['response']['type_response'] === 'danger') {
			return false
		}

	} catch (error) {
		console.log(error);
	}
}

// SUBIR LA BASE DE DATOS
$('#form').on('submit', async function(e) {
    e.preventDefault();
    if ($("#file_input").val() == null || $("#file_input").val() == '') {
        notifier.show('Ha ocurrido un error!', 'Se debe seleccionar el archivo de la base de datos', 'danger', '', 4000);
		$("#file_input").val('')
    } else {
        let parameters = new FormData(this)
        await SendJSONPetition('/recuperar-base-de-datos/', parameters)
    }

});