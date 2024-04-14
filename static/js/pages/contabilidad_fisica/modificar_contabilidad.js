let form_ingreso = document.getElementById('form_register');
let rol = document.getElementById('rol'); // Asegúrate de que este valor sea válido y exista en estados_permisos
rol = String(rol.value)

// Función para formatear la fecha
const formatearFecha = (fecha) => {
    let date = new Date(fecha);
    // Obtener el día, mes y año
    let dia = date.getDate() + 1;
    let mes = date.getMonth() + 1; // Los meses en JavaScript comienzan desde 0
    let ano = date.getFullYear();
   
    // Formatear la fecha al formato deseado
    let fechaFormateada = dia + '/' + mes + '/' + ano;
   
    return fechaFormateada;
}

let vents = {
    items : {
        estado:'',
        motivo_rechazo:'',
        det: []
    },
    sumar_contado: function () {
        this.items.det.forEach(function (c) {
            let cantidad_contada = 0;
            c.inv.forEach(function (i) {
                cantidad_contada +=i.cantidad_contada;
            });
            c.cantidad_contada = cantidad_contada;
        });
    },
    add: function (item) {
        this.items.det.push(item);
        this.list()
    },
    list: function () {
        
        tblCate = $('#detalle').DataTable({
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
                {"data": "tipo_insumo"},
                {"data": "cantidad_contada"},
                {"data": "cantidad_inventario"},
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
                    render: function (data, type, row) {

                        return data;
                    }
                },
                {
                    targets: [4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {

                        buttons = '<a href="#" rel="open_inv" class="btn btn-icon btn-dark"><i class="fa fa-briefcase"></i></a> ';                       
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {

            },
        });

    },
    list_inv: function (row) {
        
        tblInv = $('#id_datatable_inventario').DataTable({
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
            data: this.items.det[row].inv,
            columns: [
                {"data": "producto.nombre"},
                {"data": "producto.lote"},
                {"data": "producto.f_vencimiento"},
                {"data": "cantidad_contada"},
            ],
            columnDefs: [
                {
                    targets: [3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row, meta) {
                        return `<input type="number" name="cantidad_contada" min="0" value="${data}" class="form-control form-control-sm cantidad_contada" required autocomplete="off">`;
                    }
                },
                {
                    targets: [2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row, meta) {
                        return formatearFecha(data)
                    }
                },
            ],
            initComplete: function (settings, json) {

            },
        });
    },
};


let fila_productos;

$(function () {

    vents.list()

    $('#id_estado').select2({
        theme: 'bootstrap4',
        language: 'es',
        placeholder: 'Selecionar el estado',
        allowClear: true
    }).on('select2:select', function (e) {
        var data = e.params.data;
        if (data.text == 'Rechazado') {
            // Muestra el campo cuando se selecciona 'Rechazado'
            $('#id_motivo_rechazo').prop('required', true);
            $('.campo_motivo').show();
        } else {
            // Oculta el campo cuando se selecciona cualquier otro valor
            $('#id_motivo_rechazo').prop('required', false);
            $('.campo_motivo').hide();
        }
    });

    let estados_permisos = {
        'AD': [
            { 'id':'CO', 'text': 'Contabilizado' },
            { 'id':'AP', 'text': 'Aprobado' },
            { 'id':'RE', 'text': 'Rechazado' },
        ],
        'AL': [
            { 'id':'PR', 'text': 'En Proceso' },
            { 'id':'CO', 'text': 'Contabilizado' },
        ],
    }
    
    let select2 = $('#id_estado');
    let opcionesActuales = select2.find('option');
    // Verificar si el rol es válido y si tiene opciones permitidas
    if (estados_permisos[rol] && Array.isArray(estados_permisos[rol])) {
        // Obtener la opción seleccionada por defecto
        let opcionSeleccionada = select2.val();
    
        // Iterar sobre las opciones actuales
        opcionesActuales.each(function() {
            var opcionActual = $(this);
            var idActual = opcionActual.val();
            var textoActual = opcionActual.text();
    
            // Verificar si la opción actual está en el listado permitido y no es la seleccionada por defecto
            var estaPermitida = estados_permisos[rol].some(function(opcionPermitida) {
                return opcionPermitida.id === idActual && opcionPermitida.text === textoActual;
            });
    
            // Si la opción actual no está en el listado permitido y no es la seleccionada por defecto, eliminarla
            if (!estaPermitida && idActual !== opcionSeleccionada) {
                opcionActual.remove();
            }
        });
    
        // Asegurarse de que las opciones permitidas no se dupliquen
        estados_permisos[rol].forEach(function(opcionPermitida) {
            if (!opcionesActuales.filter(`[value="${opcionPermitida.id}"]`).length) {
                // Crear y agregar la nueva opción si no existe
                var newOption = new Option(opcionPermitida.text, opcionPermitida.id, false, false);
                select2.append(newOption);
            }
        });
    
        // Actualizar el Select2 para reflejar los cambios
        select2.trigger('change');
    } else {
        console.error('El rol especificado no es válido o no tiene opciones permitidas.');
    }

    $('#id_datatable_inventario tbody').on('change keyup', '.cantidad_contada', function () {
        let cantidad_contada = $(this).val();
        var tr = tblInv.cell($(this).closest('td, li')).index();
        vents.items.det[fila_productos].inv[tr.row].cantidad_contada = parseInt(cantidad_contada);
        vents.sumar_contado();
        vents.list();
    });

    /// OPEN MODAL INVENTARIO
    $('#detalle tbody').on('click', 'a[rel="open_inv"]', function () {
        var tr = tblCate.cell($(this).closest('td, li')).index();
        // var productos = tblCate.row(tr.row).data();
        vents.list_inv(tr.row);
        fila_productos = tr.row;
        $('#modal_inventario').modal('show');
    });

    // event submit
    $('#form_register').on('submit', async function (e) {
        e.preventDefault();

		vents.items.estado = $('select[name="estado"]').val();
		if (vents.items.estado == 'RE') {
			vents.items.motivo_rechazo = $('textarea[name="motivo_rechazo"]').val();
		}else{
            vents.items.motivo_rechazo = '';
        }
        console.log(vents.items);
        var parameters = new FormData();
        parameters.append('vents', JSON.stringify(vents.items));

        btn_submit.disabled = true;
        await SendDataJsonForm(window.location.pathname, parameters, function () {
            window.location.replace('/listado-de-ajustes-de-inventario-fisico/');
        });
    });
});