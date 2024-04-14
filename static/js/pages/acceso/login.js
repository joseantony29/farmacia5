// CONFIG FORM
const SendDataJSONForm = async (url, form, callback) => {
	try {
		const formData = new FormData(form);

		const response = await fetch (url, {
			method: "POST",
			body: formData
		});
		const data = await response.json();

		notifier.show(data['response']['title'], data['response']['data'], data['response']['type_response'], '', 4000);
		if (data['response']['type_response'] === 'danger') {
			console.log(data);
			return false
		}

		callback();

	} catch (error) {
		notifier.show('Ocurrió un error!', error, 'danger', '', 4000);
		console.log(error);
	}
}

// FORM VIEW LOGIC

let form_login = document.getElementById('form_login');

$( async function () {

	// LOGIN SEND FORM
	form_login.addEventListener('submit', async (e) => {
        e.preventDefault();
        await SendDataJSONForm(window.location.pathname, form_login, async () => {  
            setTimeout(() => {
                window.location.replace('/inicio/');
            }, 1000); // Espera 3 segundos antes de ejecutar el código dentro de setTimeout
        });
    });
    

});

$('#btn_pass_show').click(function() {
	// Obtiene el input de contraseña
	var passwordInput = $('#password2');
	// Verifica si el tipo de input es 'password'
	if (passwordInput.attr('type') === 'password') {
		// Cambia el tipo de input a 'text' para mostrar la contraseña
		passwordInput.attr('type', 'text');
		// Cambia el icono del ojo a cerrado
		$(this).html('<i class="fa fa-eye-slash"></i>');
	} else {
		// Cambia el tipo de input a 'password' para ocultar la contraseña
		passwordInput.attr('type', 'password');
		// Cambia el icono del ojo a abierto
		$(this).html('<i class="fa fa-eye"></i>');
	}
});