let form_edit_info = document.getElementById('form_edit_info');
let form_nuevo_bene = document.getElementById('form_nuevo_bene');
let form_edit_bene = document.getElementById('form_edit_bene');

let getData = async () => {
    // PROVIDERS LIST
    await getDataTable(
        // paging
        true,
        // searching
        true,
        // ordering
        true,
        '#listado_beneficiados',
        {
            'action': 'search_beneficiados',
        },
        [
            {"data": "cedula"},
            {"data": "nombres"},
            {"data": "apellidos"},
            {"data": "genero"},
            {"data": "f_nacimiento"},
            {"data": "embarazada"},
            {"data": "id"},
        ],
        [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let buttons = '<a href="#" rel="edit" class="btn btn-icon btn-dark" data-bs-toggle="tooltip" data-bs-placement="top" title="Editar Beneficiado"><i class="fa fa-edit"></i></a>';
                    return buttons
                }
            },{
                targets: [-2],
                class: 'text-center',
                orderable: true,
                render: function (data, type, row) {
                    if(data == 'True'){
                        return 'SI';
                    } else if(row['genero'] == 'Masculino'){ 
                        return 'NO APLICA';
                    } else {
                        return 'NO';
                    }
                }
            }
        ],
        '/mi-perfil/'
    );
}

$( async function () {
    await getData();

    form_edit_info.addEventListener('submit', async (e) => {
        e.preventDefault();
        let parameters = new FormData(form_edit_info);

        await SendDataJsonForm(type_actions['perfil_edit'][action_edit.value], parameters, async () => {  
            await getData();
            $('#smallmodal').modal('hide');   
            $("#form_edit_info")[0].reset(); 
            window.location.reload();
        });
    });

    form_nuevo_bene.addEventListener('submit', async (e) => {
        e.preventDefault();
        let parameters = new FormData(form_nuevo_bene);
        
        await SendDataJsonForm(type_actions['benefi'][action_bene.value], parameters, async () => {  
            await getData();
            $('#modal_nuevo_bene').modal('hide');   
            $("#form_nuevo_bene")[0].reset(); 
        });
    });

    // REGISTER USUARIO
    $('#btn_edit_info').on('click', function () {
        $('input[name="action_edit"]').val('editar_info');
        $('#smallmodal').modal('show');
    });

    $('#btn_nuevo_bene').on('click', function () {
        $('input[name="action"]').val('nuevo_bene');
        $('#modal_nuevo_bene').modal('show');
    });

    $('#listado_beneficiados tbody').on('click', 'a[rel="edit"]', function () {
        $('#form_edit_bene')[0].reset();
        $('#modal_edit_bene').modal('show');   
        var tr = tblCate.cell($(this).closest('td, li')).index();
        var data = tblCate.row(tr.row).data();

        $('input[name="action"]').val('editar_bene');
        $('input[name="id"]').val(data.cedula);
        $('input[name="telefono_bene"]').val(data.telefono);
        $('select[name="parentesco"]').val(data.parentesco);
        $('select[name="zona_bene"]').val(data.zona.id);
        $('textarea[name="direccion_bene"]').val(data.direccion);
        $('textarea[name="patologia_bene"]').val(data.patologia);
        $('input[name="c_residencia_bene"]').val(data.c_residencia);
        

        if(data.embarazada == 'True'){
            $('input[name="embarazada_bene"]').prop('checked', true)
        }else{
            $('input[name="embarazada_bene"]').prop('checked', false)
        }

    });

    form_edit_bene.addEventListener('submit', async (e) => {
        e.preventDefault();
        let parameters = new FormData(form_edit_bene);
        
        await SendDataJsonForm(type_actions['benefi'][action.value], parameters, async () => {  
            await getData();
            $('#modal_edit_bene').modal('hide');   
            $("#form_edit_bene")[0].reset(); 
        });
    });

    $('#id_genero').change(function () {
        if ($(this).val() == "MA") {
            // Deshabilitar checkboxes
            $('.deshabilitar').prop('disabled', true);
            $('#inline-radio2').prop('checked', true)
        } else {
            // Habilitar checkboxes
            $('.deshabilitar').prop('disabled', false);
        }
    }).trigger('change'); // Trigger para establecer el estado inicial
});