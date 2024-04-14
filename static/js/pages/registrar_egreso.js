let form_ingreso = document.getElementById('form_register');
let form_search = document.getElementById('search-input');

let fechaHoy = new Date();
let dia = fechaHoy.getDate();
let mes = fechaHoy.getMonth() + 1; // Los meses en JavaScript comienzan en 0
let año = fechaHoy.getFullYear();

// Asegurarse de que el día y el mes tengan dos dígitos
if (dia < 10) dia = '0' + dia;
if (mes < 10) mes = '0' + mes;

// Formatear la fecha en el formato YYYY-MM-DD
let fechaFormateada = año + '-' + mes + '-' + dia;

let vents = {
    items : {
        fecha: '',
        descripcion: '',
        tipo_egreso: '',
        det: []
    },
    get_ids: function () {
        var ids =  [];
        $.each(this.items.det, function (key, value) {
            ids.push(value.id_lote);
        });
        return ids;
    },
    add: function (item) {
        this.items.det.push(item);
        this.list()
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
                {"data": "tipo_insumo.nombre"},
                {"data": "almacen.nombre"},
                {"data": "total_stock"},
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
            '/buscar-productos-egresos/'
        );
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
                {"data": "id_lote"},
                {"data": "f_vencimiento"},
                {"data": "stock"},
                {"data": "cantidad"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row, meta) {                        
                        if (data) {
                            var selectOptions =`<option value="${data}">${row.lote}</option>`;
                        }else{                        // Añade una opción vacía al principio
                            var selectOptions ='<option value="">Selecciona una opción</option>';
                            for (var i = 0; i < row.others.inv.lotes.length; i++) {
                                selectOptions +='<option value="'+row.others.inv.lotes[i].id+'">'+row.others.inv.lotes[i].text+'</option>';
                            }
                        }
                        return '<select class="form-control lotes" required>'+selectOptions+'</select>';
                    }
                },
                {
                    targets: [4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row, meta) {                        
                        return `<input type="number" value="${parseInt(data)}" name="cantidad" class="form-control form-control-sm cantidad" required min="1" max="${parseInt(row.stock)}" autocomplete="off">`;
                    }
                },
                {
                    targets: [5],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {

                        buttons = '<a href="#" rel="delete" class="btn btn-icon btn-danger"><i class="fa fa-trash"></i></a> ';                       
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {
                $('.lotes').select2({
                    theme: 'bootstrap4',
                    language: 'es',
                    placeholder: 'Selecionar la cantidad',
                    allowClear: true
                });
            },
        });

    },
};

document.addEventListener('DOMContentLoaded', function() {   
    // Establecer los atributos min y max del input
    let inputFecha = document.getElementById('id_fecha');
    inputFecha.setAttribute('min', fechaFormateada);
    inputFecha.setAttribute('max', fechaFormateada);
    inputFecha.value = fechaFormateada;
});

$('#id_tipo_egreso').select2({
    theme: 'bootstrap4',
    language: 'es',
    placeholder: 'Selecionar tipo de egreso',
    allowClear: true
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
        '<b style="color:#000000">Disponibilidad:</b> <b style="color:#000000">' + repo.others.total_stock + '</b><br>' +
        '</p>' +
        '</div>');

    return option;
}

$(function () {

    vents.list()

    // auto complete search
    $('select[name="search"]').select2({
        theme: "bootstrap4",
        language: "es",
        allowClear: true,
        ajax: {
            delay: 250,
            type: "POST", 
            url: '/buscar-productos-egresos/',
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
                        others: res
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
        data.stock = ""
        data.f_vencimiento = "-";
        data.lote = "";
        data.id_lote = "";
        vents.add(data);
        $(this).val('').trigger('change.select2');
    });

    $('#detalle tbody').on('change', '.lotes', function () {
        let lote = $(this).val();
        if (lote) {
            // Obtiene el índice de la fila de la celda seleccionada
            var tr = $(this).closest('tr');
            var rowIndex = tblCate.row(tr).index();
        
            // Usa el índice de la fila para obtener los datos de la fila
            let prod = tblCate.row(rowIndex).data();
            vents.items.det[rowIndex].f_vencimiento = prod['others']['inv']['datos'][lote]['fecha_vencimiento']
            vents.items.det[rowIndex].stock = prod['others']['inv']['datos'][lote]['stock']
            vents.items.det[rowIndex].id_lote = prod['others']['inv']['datos'][lote]['id']
            vents.items.det[rowIndex].lote = prod['others']['inv']['datos'][lote]['lote']
            vents.list();
        }

    });

    // asignar valor cantidad
    $('#detalle tbody').on('change keyup', '.cantidad', function () {
        let cantidad = $(this).val();
        var tr = tblCate.cell($(this).closest('td, li')).index();
        vents.items.det[tr.row].cantidad = parseInt(cantidad);
    });

    // delete individual element
    $('#detalle tbody').on('click', 'a[rel="delete"]', function () {
        var tr = tblCate.cell($(this).closest('td, li')).index();
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
    /** OPEN MODAL PRODUCT **/
    $('a[rel="open_modal_product"]').on('click', function () {
        vents.search_productos()
        $('#modal_search_product').modal('show');
    });
    // PRODUCT SELECT
    $('#id_datatable_productos tbody').on('click', 'a[rel="select_product"]', function () {
        var tr = tblCate.cell($(this).closest('td, li')).index();
        var productos = tblCate.row(tr.row).data();
        let data = {
            id: productos.id,
            text: productos.nombre,
            stock: "",
            f_vencimiento: "-",
            lote:"",
            id_lote:"",
            nombre: productos.nombre,
            others: productos,
            cantidad: 1,
        }
        vents.add(data);
        $('#modal_search_product').modal('hide');   
    });
    // event submit
    $('#form_register').on('submit', async function (e) {
        e.preventDefault();
        
        if (vents.items.det.length === 0) {
            notifier.show('Ocurrio un error!', 'Debe al menos tener un producto en el egreso', 'danger', '', 4000);
            return false;
        }
    
        const rastreador = {};
        let repetido = false;
    
        for (const item of vents.items.det) {
            if (rastreador[item.id_lote]) {
                notifier.show('Ocurrio un error!', 'El lote se repite, solo puede seleccionar un lote diferente por producto', 'danger', '', 4000);
                repetido = true;
                break; // Detiene la ejecución del bucle
            } else {
                rastreador[item.id_lote] = true;
            }
        }
    
        if (repetido) {
            return false; // Detiene el envío del formulario si se encontró un lote repetido
        }
    
        vents.items.descripcion = $('textarea[name="descripcion"]').val();
        vents.items.fecha = $('input[name="fecha"]').val();
        vents.items.tipo_egreso = $('select[name="tipo_egreso"]').val();
    
        var parameters = new FormData();
        parameters.append('vents', JSON.stringify(vents.items));
    
        btn_submit.disabled = true;
    
        await SendDataJsonBuyForm(window.location.pathname, parameters, function () {
            window.location.replace('/listado-de-egresos/');
        })
    });
});