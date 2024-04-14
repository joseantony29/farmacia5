let form_ingreso = document.getElementById('form_register');

// Función para formatear la fecha
const formatearFecha = (fecha) => {
    let date = new Date(fecha);
    // Obtener el día, mes y año
    let dia = date.getDate();
    let mes = date.getMonth() + 1; // Los meses en JavaScript comienzan desde 0
    let ano = date.getFullYear();
   
    // Formatear la fecha al formato deseado
    let fechaFormateada = dia + '/' + mes + '/' + ano;
   
    return fechaFormateada;
}

let vents = {
    items : {
        det: []
    },
    sumar_contado: function () {
        this.items.det.forEach(function (c) {
            let cantidad_contada = 0;
            c.inv.forEach(function (i) {
                cantidad_contada +=i.cantidad_contada;
            });
            c.cantidad = cantidad_contada;
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
                    render: function (data, type, row) {

                        return data;
                    }
                },
                {
                    targets: [3],
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
                {"data": "nombre"},
                {"data": "lote"},
                {"data": "f_vencimiento"},
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

$(async function () {
    
    const CargarProductos = async (callback) => {
        try {
            let parameters = new FormData()
            parameters.append('action', 'cargar_productos')    
            const response = await fetch ('/buscar-productos-validados/', {
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
    // CARGAR TODOS LOS PRODUCTOS
    let producto = await CargarProductos(()=>{
    });
    producto.forEach(function (c) {
        vents.add(c);
    });
    vents.list();

});

let fila_productos;

$(function () {

    vents.list()

    // asignar valor cantidad
    $('#detalle tbody').on('change keyup', '.cantidad', function () {
        let cantidad = $(this).val();
        var tr = tblCate.cell($(this).closest('td, li')).index();
        vents.items.det[tr.row].cantidad = parseInt(cantidad);
    });

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
        
        if (vents.items.det.length === 0) {
            notifier.show('Ocurrio un error!', 'Debe al menos tener un producto en la solicitud', 'danger', '', 4000);
            return false;
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