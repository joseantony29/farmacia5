let form_ingreso = document.getElementById('form_register');
let form_search = document.getElementById('search-input');
let perfil_id = document.getElementById('perfil_id');

let vents = {
    items : {
        descripcion: '',
        det: [],
        beneficiados: []
    },
    get_ids: function () {
        var ids =  [];
        $.each(this.items.det, function (key, value) {
            ids.push(value.id);
        });
        return ids;
    },
    get_ids_beneficiados: function () {
        var ids =  [];
        $.each(this.items.beneficiados, function (key, value) {
            ids.push(value.id);
        });
        return ids;
    },
    add: function (item) {
        this.items.det.push(item);
        this.list()
    },
    add_beneficiados: function (item) {
        this.items.beneficiados.push(item);
        this.list_beneficiados()
    },
    search_productos: async function () {
        /** PRODUCT LIST **/
        await getDataTable(
            // paging
            true,
            // searching
            true,
            // ordering
            true,
            '#id_datatable_productos',
            {
                'action': 'search_productos_table',
                'ids': JSON.stringify(vents.get_ids()),
            },
            [
                {"data": "nombre"},
                {"data": "id"},
            ],
            [
                {
                    targets: [-1],
                    orderable: false,
                    render: function (data, type, row) {
                        let buttons = '<a href="#" rel="select_product" class="btn btn-icon btn-dark" data-bs-toggle="tooltip" title="Seleccionar producto"><i class="fa fa-hand-o-up"></i></a>';
                        return buttons
                    }
                },
            ],
            '/buscar-productos/'
        );
    },
    search_beneficiados: async function () {
        /** PRODUCT LIST **/
        await getDataTable(
            // paging
            true,
            // searching
            true,
            // ordering
            true,
            '#id_datatable_beneficiados',
            {
                'action': 'search_beneficiados_table',
                'ids': JSON.stringify(vents.get_ids_beneficiados()),
            },
            [
                {"data": "cedula"},
                {"data": "nombres"},
                {"data": "apellidos"},
                {"data": "patologia"},
                {"data": "id"},
            ],
            [
                {
                    targets: [-1],
                    orderable: false,
                    render: function (data, type, row) {
                        let buttons = '<a href="#" rel="select_beneficiado" class="btn btn-icon btn-dark" data-bs-toggle="tooltip" title="Seleccionar beneficiado"><i class="fa fa-hand-o-up"></i></a>';
                        return buttons
                    }
                },
            ],
            '/cargar-comunidad/'
        );
    },
    list: function () {
        
        tblMedi = $('#detalle').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ordering:  false,
            searching: false,
            paging: false,
            "language": {
                "sProcessing": "Procesando...",
                "sLengthMenu": "Mostrar _MENU_ registros",
                "sZeroRecords": "No se encontraron resultados",
                "sEmptyTable": "Ningún dato disponible en esta tabla",
                "sInfo": "Mostrando _START_ al _END_ de un total de _TOTAL_ registros",
                "sInfoEmpty": "Mostrando 0 al 0 de un total de 0 registros",
                "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
                "sInfoPostFix": "",
                "sSearch": "Buscar:",
                "sUrl": "",
                "sInfoThousands": ",",
                "sLoadingRecords": "Cargando...",
                "oPaginate": {
                    "sFirst": "<span class='fa fa-angle-double-left'></span>",
                    "sLast": "<span class='fa fa-angle-double-right'></span>",
                    "sNext": "<span class='fa fa-angle-right'></span>",
                    "sPrevious": "<span class='fa fa-angle-left'></span>"
                },
                "oAria": {
                    "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
                    "sSortDescending": ": Activar para ordenar la columna de manera descendente"
                }
            },
            data: this.items.det,
            columns: [
                {"data": "nombre"},
                {"data": "cantidad"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {

                        return data;
                    }
                },
                {
                    targets: [1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row, meta) {                        
                        return '<input type="number" value="'+ parseInt(data) +'" name="cantidad" class="form-control form-control-sm cantidad" required min="1" autocomplete="off">';
                    }
                },
                {
                    targets: [2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {

                        buttons = '<a href="#" rel="delete" class="btn btn-icon btn-danger"><i class="fa fa-trash"></i></a> ';                       
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {

            },
        });

    },
    list_beneficiados: function () {
        
        tblBene = $('.detalle').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ordering:  false,
            searching: false,
            paging: false,
            "language": {
                "sProcessing": "Procesando...",
                "sLengthMenu": "Mostrar _MENU_ registros",
                "sZeroRecords": "No se encontraron resultados",
                "sEmptyTable": "Ningún dato disponible en esta tabla",
                "sInfo": "Mostrando _START_ al _END_ de un total de _TOTAL_ registros",
                "sInfoEmpty": "Mostrando 0 al 0 de un total de 0 registros",
                "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
                "sInfoPostFix": "",
                "sSearch": "Buscar:",
                "sUrl": "",
                "sInfoThousands": ",",
                "sLoadingRecords": "Cargando...",
                "oPaginate": {
                    "sFirst": "<span class='fa fa-angle-double-left'></span>",
                    "sLast": "<span class='fa fa-angle-double-right'></span>",
                    "sNext": "<span class='fa fa-angle-right'></span>",
                    "sPrevious": "<span class='fa fa-angle-left'></span>"
                },
                "oAria": {
                    "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
                    "sSortDescending": ": Activar para ordenar la columna de manera descendente"
                }
            },
            data: this.items.beneficiados,
            columns: [
                {"data": "cedula"},
                {"data": "nombres"},
                {"data": "apellidos"},
                {"data": "patologia"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {

                        buttons = '<a href="#" rel="delete" class="btn btn-icon btn-danger"><i class="fa fa-trash"></i></a> ';                       
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {

            },
        });

    },
};

const CargarTodaComunidad = async (callback) => {
	try {
        let parameters = new FormData()
        parameters.append('action', 'search_beneficiados_table')
        parameters.append('ids', JSON.stringify(vents.get_ids_beneficiados()))

        const response = await fetch ('/cargar-comunidad/', {
			method: "POST",
			body: parameters
		});
		const data = await response.json();
        return data
		callback();

	} catch (error) {
		notifier.show('Ocurrió un error!', error, 'danger', '', 4000);
		console.log(error);
	}
}
// CARGAR TODA LA COMUNIDAD
$('a[rel="btn_select_all_b"]').on('click',async function () {3
    let comunidad = await CargarTodaComunidad(()=>{
    });
    comunidad.forEach(function (c) {
        vents.add_beneficiados(c);
        vents.search_beneficiados();
    });
    vents.list_beneficiados();
    notifier.show('Exito!', 'La comunidad se ha cargado correctamente', 'success', '', 4000);
    $('#modal_search_beneficiado').modal('hide');   

});

// FORMATTING WHEN DISPLAYING THE RESULT OF THE SELECT
function formatRepo(repo) {
    if (repo.loading) {
        return repo.text;
    }

    let option = $(
        '<div class="col text-left shadow-sm">' +
        '<p style="margin-bottom: 0;">' +
        '<b style="color:#000000">Nombre:</b> <b style="color:#000000">' + repo.text+ '</b><br>' +
        '<b style="color:#000000">Codigo:</b> <b style="color:#000000">' + repo.id + '</b><br>' +
        '</p>' +
        '</div>');

    return option;
}
// FORMATTING WHEN DISPLAYING THE RESULT OF THE SELECT
function formatRepoBeneficiado(repo) {
    if (repo.loading) {
        return repo.text;
    }

    let option = $(
        '<div class="col text-left shadow-sm">' +
        '<p style="margin-bottom: 0;">' +
        '<b style="color:#000000">Cedula:</b> <b style="color:#000000">' + repo.cedula+ '</b><br>' +
        '<b style="color:#000000">Nombre:</b> <b style="color:#000000">' + repo.nombres + '</b><br>' +
        '<b style="color:#000000">Apellido:</b> <b style="color:#000000">' + repo.apellidos + '</b><br>' +
        '</p>' +
        '</div>');

    return option;
}

$(function () {

    vents.list()
    vents.list_beneficiados()

    // auto complete search
    $('select[name="search"]').select2({
        theme: "bootstrap4",
        language: "es",
        allowClear: true,
        ajax: {
            delay: 250,
            type: "POST", 
            url: '/buscar-productos/',
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: "search_productos",
                    ids: JSON.stringify(vents.get_ids())
                }
                return queryParameters;
            },
            processResults: function (data) {
                var results = [];
              
                $.each(data, function (index, res) {
                    results.push({
                        id: res.id,
                        text: res.nombre,
                    });
                });
    
                return {
                    results: results
                };
            },
            cache: true

        },
        placeholder: 'Buscar producto ...', 
        minimumInputLength: 1,
        templateResult: formatRepo,
    }).on('select2:select', function (e) {
        var data = e.params.data;
        data.cantidad = 1;
        data.nombre = data.text;
        vents.add(data);
        $(this).val('').trigger('change.select2');
    });

    // auto complete search
    $('select[name="search_beneficiados"]').select2({
        theme: "bootstrap4",
        language: "es",
        allowClear: true,
        ajax: {
            delay: 250,
            type: "POST", 
            url: '/cargar-comunidad/',
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: "search_beneficiados",
                    ids: JSON.stringify(vents.get_ids_beneficiados())
                }
                return queryParameters;
            },
            processResults: function (data) {
                var results = [];
              
                $.each(data, function (index, res) {
                    results.push({
                        id: res.id,
                        text: res.nombres,
                        cedula: res.cedula,
                        nombres: res.nombres,
                        apellidos: res.apellidos,
                        patologia: res.patologia,
                    });
                });
                return {
                    results: results
                };
            },
            cache: true

        },
        placeholder: 'Buscar beneficiado ...', 
        minimumInputLength: 1,
        templateResult: formatRepoBeneficiado,
    }).on('select2:select', function (e) {
        var data = e.params.data;
        console.log(data);
        vents.add_beneficiados(data);
        $(this).val('').trigger('change.select2');
    });

    // asignar valor cantidad
    $('#detalle tbody').on('change keyup', '.cantidad', function () {
        let cantidad = $(this).val();
        var tr = tblMedi.cell($(this).closest('td, li')).index();
            vents.items.det[tr.row].cantidad = parseInt(cantidad);
    });

    // delete individual element
    $('#detalle tbody').on('click', 'a[rel="delete"]', function () {
        var tr = tblMedi.cell($(this).closest('td, li')).index();
        vents.items.det.splice(tr.row, 1);
        vents.list();
        notifier.show('Exito!', 'Se ha eliminado correctamente', 'success', '', 4000);
    });
    /// remove all detail
    $('a[rel="btn_delete"]').on('click', function () {
        if (vents.items.det.length === 0) return false;
        vents.items.det = [];
        vents.list();
        notifier.show('Exito!', 'Se ha eliminado correctamente', 'success', '', 4000);
    });

    // delete individual element beneficiados
    $('.detalle tbody').on('click', 'a[rel="delete"]', function () {
        var tr = tblBene.cell($(this).closest('td, li')).index();
        vents.items.beneficiados.splice(tr.row, 1);
        vents.list_beneficiados();
        notifier.show('Exito!', 'Se ha eliminado correctamente', 'success', '', 4000);
    });
    /// remove all detail beneficiados
    $('a[rel="btn_delete_b"]').on('click', function () {
        if (vents.items.beneficiados.length === 0) return false;
        vents.items.beneficiados = [];
        vents.list_beneficiados();
        notifier.show('Exito!', 'Se ha eliminado correctamente', 'success', '', 4000);
    });

    /** OPEN MODAL PRODUCT **/
    $('a[rel="open_modal_product"]').on('click', function () {
        vents.search_productos()
        $('#modal_search_product').modal('show');
    });

    /** OPEN MODAL BENEFICIADO **/
    $('a[rel="open_modal_beneficiados"]').on('click', function () {
        vents.search_beneficiados()

        $('#modal_search_beneficiado').modal('show');
    });

    // PRODUCT SELECT
    $('#id_datatable_productos tbody').on('click', 'a[rel="select_product"]', function () {
        var tr = tblCate.cell($(this).closest('td, li')).index();
        var productos = tblCate.row(tr.row).data();
        let data = {
            id: productos.id,
            text: productos.nombre,
            nombre: productos.nombre,
            cantidad: 1,
        }
        vents.add(data);
        $('#modal_search_product').modal('hide');   
    });

    // BENEFICIADO SELECT
    $('#id_datatable_beneficiados tbody').on('click', 'a[rel="select_beneficiado"]', function () {
        var tr = tblCate.cell($(this).closest('td, li')).index();
        let beneficiados = tblCate.row(tr.row).data();
        let data = {
            id: beneficiados.id,
            text: beneficiados.nombres,
            cedula: beneficiados.cedula,
            nombres: beneficiados.nombres,
            apellidos: beneficiados.apellidos,
            patologia: beneficiados.patologia,
        }
        vents.add_beneficiados(data);
        vents.search_beneficiados()
    });

    $('#btn_medicamentos').on('click', function () {
        if (btn_medicamentos.textContent === 'Ocultar') {
            btn_medicamentos.textContent = 'Mostrar';
            // Aquí puedes agregar el código para ocultar los medicamentos solicitados
        } else {
            btn_medicamentos.textContent = 'Ocultar';
            // Aquí puedes agregar el código para mostrar los medicamentos solicitados
        }
    });

    $('#btn_beneficiados').on('click', function () {
        console.log('hola');

        if (btn_beneficiados.textContent === 'Ocultar') {
            btn_beneficiados.textContent = 'Mostrar';
            // Aquí puedes agregar el código para ocultar los medicamentos solicitados
        } else {
            btn_beneficiados.textContent = 'Ocultar';
            // Aquí puedes agregar el código para mostrar los medicamentos solicitados
        }
    });

    // event submit
    $('#form_register').on('submit', async function (e) {
        e.preventDefault();
        
        if (vents.items.det.length === 0) {
            notifier.show('Ocurrio un error!', 'Debe al menos tener un producto en la solicitud', 'danger', '', 4000);
            return false;
        }

        if (vents.items.beneficiados.length === 0) {
            notifier.show('Ocurrio un error!', 'Debe al menos tener un miembro de la comunidad en la jornada', 'danger', '', 4000);
            return false;
        }

        vents.items.descripcion = $('textarea[name="descripcion"]').val();
        // return false;
        var parameters = new FormData();
        parameters.append('vents', JSON.stringify(vents.items));
        console.log(vents.items);
        btn_submit.disabled = true;
        await SendDataJsonForm(window.location.pathname, parameters, function () {
            window.location.replace('/mis-solicitudes-de-jornadas/');
        })
    });
});