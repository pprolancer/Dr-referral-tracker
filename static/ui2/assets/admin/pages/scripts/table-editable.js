var TableEditable = function () {

    var handleTable = function () {

        function restoreRow(oTable, nRow) {
            var aData = oTable.fnGetData(nRow);
            var jqTds = $('>td', nRow);

            for (var i = 0, iLen = jqTds.length; i < iLen; i++) {
                oTable.fnUpdate(aData[i], nRow, i, false);
            }

            oTable.fnDraw();
        }
		function validateEdit(){
			console.log($("#orgForm"));
			
			$("#orgForm").validate({
				rule:{
					orgName:{
						required: true,
      					maxlength: 254	
					},
					orgType:{
						required: true
					},
					orgContactName:{
						required: true,
      					maxlength: 254	
					},
					orgPhone:{
						number: true
					},
					orgEmail:{
						 email: true	
					},
					orgSpecial:{
							
					}

				},
				messages:{
					orgName:{
						required: "Please provide the Organization Name",
      					maxlength: "Organization Name should not exceed 254 charactors. "	
					},
					orgType:{
						required: "Please Select the Organization Type"
					},
					orgContactName:{
						required: "Please provide the Organization Contact Name",
      					maxlength: "Organization Contact Name should not exceed 254 charactors. "	
					},
					orgPhone:{
						number: "Phonne number should have only numiric charactors"
					},
					orgEmail:{
						 email: "please enter a valied email adress"	
					},
					orgSpecial:{
						
					}
				}
			})
			
		}
		
		function validateNew(){
			
			
			
		}

        function editRow(oTable, nRow) {
            var aData = oTable.fnGetData(nRow);
            var jqTds = $('>td', nRow);
            //jqTds[0].innerHTML = '<input type="text" class="form-control " value="' + aData[0] + '">';
            jqTds[1].innerHTML = '<input id="orgName" name="orgName" type="text" class="form-control " required value="' + aData[1] + '">';
            jqTds[2].innerHTML = '<select id="orgType" name="orgType" class="form-control" required><option value="MAR">Marketing</option><option value="INS">Insurance</option><option value="INT">Internal</option><option value="WKC">Work comp.</option><option value="HCP">Healthcare Provider</option></select>';
            jqTds[3].innerHTML = '<input id="orgContactName" name="orgContactName" type="text" class="form-control " value="' + aData[3] + '" required>';
			jqTds[4].innerHTML = '<input id="orgPhone" name="orgPhone" type="text" class="form-control " value="' + aData[4] + '">';
			jqTds[5].innerHTML = '<input id="orgEmail" name="orgEmail" type="email" class="form-control " value="' + aData[5] + '">';
			jqTds[6].innerHTML = '<select id="orgSpecial" name="orgSpecial" class="form-control"><option value="true">True</option><option value="false">False</option></select>';
            jqTds[7].innerHTML = '<a class="edit" href="">Save</a>';
			jqTds[8].innerHTML = '<a class="cancel" href="">Cancel</a>';
            validateEdit()
        }
		
		function createRow(oTable, nRow) {
            var aData = oTable.fnGetData(nRow);
            var jqTds = $('>td', nRow);
            jqTds[0].innerHTML = '<input type="text" class="form-control " value="' + aData[0] + '">';
           jqTds[1].innerHTML = '<input id="orgName" name="orgName" type="text" class="form-control " required value="' + aData[1] + '">';
            jqTds[2].innerHTML = '<select id="orgType" name="orgType" class="form-control" required><option value="MAR">Marketing</option><option value="INS">Insurance</option><option value="INT">Internal</option><option value="WKC">Work comp.</option><option value="HCP">Healthcare Provider</option></select>';
            jqTds[3].innerHTML = '<input id="orgContactName" name="orgContactName" type="text" class="form-control " value="' + aData[3] + '" required>';
			jqTds[4].innerHTML = '<input id="orgPhone" name="orgPhone" type="text" class="form-control " value="' + aData[4] + '">';
			jqTds[5].innerHTML = '<input id="orgEmail" name="orgEmail" type="email" class="form-control " value="' + aData[5] + '">';
			jqTds[6].innerHTML = '<select id="orgSpecial" name="orgSpecial" class="form-control"><option value="true">True</option><option value="false">False</option></select>';
            jqTds[7].innerHTML = '<a class="edit" href="">Save</a>';
			jqTds[8].innerHTML = '<a class="cancel" href="">Cancel</a>';
			
            validateNew()
        }

        function saveRow(oTable, nRow) {
            var jqInputs = $('input', nRow);
            //oTable.fnUpdate(jqInputs[0].value, nRow, 0, false);
            oTable.fnUpdate(jqInputs[0].value, nRow, 1, false);
            oTable.fnUpdate(jqInputs[1].value, nRow, 2, false);
            oTable.fnUpdate(jqInputs[2].value, nRow, 3, false);
			oTable.fnUpdate(jqInputs[3].value, nRow, 4, false);
            oTable.fnUpdate(jqInputs[4].value, nRow, 5, false);
            oTable.fnUpdate(jqInputs[5].value, nRow, 6, false);
            oTable.fnUpdate('<a class="edit" href="">Edit</a>', nRow, 7, false);
            oTable.fnUpdate('<a class="delete" href="">Delete</a>', nRow, 8, false);
            oTable.fnDraw();
        }

        function cancelEditRow(oTable, nRow) {
            var jqInputs = $('input', nRow);
            //oTable.fnUpdate(jqInputs[0].value, nRow, 0, false);
            oTable.fnUpdate(jqInputs[0].value, nRow, 1, false);
            oTable.fnUpdate(jqInputs[1].value, nRow, 2, false);
            oTable.fnUpdate(jqInputs[2].value, nRow, 3, false);
			oTable.fnUpdate(jqInputs[3].value, nRow, 4, false);
            oTable.fnUpdate(jqInputs[4].value, nRow, 5, false);
            oTable.fnUpdate(jqInputs[5].value, nRow, 6, false);
            oTable.fnUpdate('<a class="edit" href="">Edit</a>', nRow, 7, false);
            oTable.fnDraw();
        }
		function validateInput(nRow){
			var jqInputs = $('input', nRow);
			var validated ={};
			
			if(jqInputs[0].value.length >254){
				
			}
			if(jqInputs[0].value.length >254){
				
			}
			if(jqInputs[0].value.length >10){
				
			}
			if(jqInputs[0].value.length >254){
				
			}
			if(jqInputs[0].value.length >254){
				
			}

		}
		
        var table = $('#sample_editable_1');

        var oTable = table.dataTable({

            // Uncomment below line("dom" parameter) to fix the dropdown overflow issue in the datatable cells. The default datatable layout
            // setup uses scrollable div(table-scrollable) with overflow:auto to enable vertical scroll(see: assets/global/plugins/datatables/plugins/bootstrap/dataTables.bootstrap.js). 
            // So when dropdowns used the scrollable div should be removed. 
            //"dom": "<'row'<'col-md-6 col-sm-12'l><'col-md-6 col-sm-12'f>r>t<'row'<'col-md-5 col-sm-12'i><'col-md-7 col-sm-12'p>>",

            "lengthMenu": [
                [5, 15, 20, -1],
                [5, 15, 20, "All"] // change per page values here
            ],

            // Or you can use remote translation file
            ///"language": {
              // url: '../../api/v1/organization/'
           // },
		   /*"processing": true,
		   
		   "ajax": "../../api/v1/organization/",
			"columns": [
				{ "data": "results.id" },
				{ "data": "results.org_name	" },
				{ "data": "results.org_type" },
				{ "data": "results.org_contact_name" },
				{ "data": "results.org_phone" },
				{ "data": "results.org_email" },
				{ "data": "results.org_special" }
			],*/

            // set the initial value
            "pageLength": 5,
			
			

            "language": {
                "lengthMenu": " _MENU_ records"
            },
            "columnDefs": [{ // set default column settings
                'orderable': true,
                'targets': [0]
            }, {
                "searchable": true,
                "targets": [0]
            }],
            "order": [
                [0, "asc"]
            ] // set first column as a default sort by asc
        });

        var tableWrapper = $("#sample_editable_1_wrapper");

        tableWrapper.find(".dataTables_length select").select2({
            showSearchInput: false //hide search box with special css class
        }); // initialize select2 dropdown

        var nEditing = null;
        var nNew = false;

        $('#sample_editable_1_new').click(function (e) {
            e.preventDefault();

            if (nNew && nEditing) {
                if (confirm("Previose row not saved. Do you want to save it ?")) {
                    saveRow(oTable, nEditing); // save
                    $(nEditing).find("td:first").html("Untitled");
                    nEditing = null;
                    nNew = false;

                } else {
                    oTable.fnDeleteRow(nEditing); // cancel
                    nEditing = null;
                    nNew = false;
                    return;
                }
            }

            var aiNew = oTable.fnAddData(['', '', '', '', '', '', '', '', '', '']);
            var nRow = oTable.fnGetNodes(aiNew[0]);
            createRow(oTable, nRow);
            nEditing = nRow;
            nNew = true;
        });

        table.on('click', '.delete', function (e) {
            e.preventDefault();

            if (confirm("Are you sure to delete this row ?") == false) {
                return;
            }

            var nRow = $(this).parents('tr')[0];
            oTable.fnDeleteRow(nRow);
            alert("Deleted! Do not forget to do some ajax to sync with backend :)");
        });

        table.on('click', '.cancel', function (e) {
            e.preventDefault();
            if (nNew) {
                oTable.fnDeleteRow(nEditing);
                nEditing = null;
                nNew = false;
            } else {
                restoreRow(oTable, nEditing);
                nEditing = null;
            }
        });

        table.on('click', '.edit', function (e) {
            e.preventDefault();

            /* Get the row as a parent of the link that was clicked on */
            var nRow = $(this).parents('tr')[0];

            if (nEditing !== null && nEditing != nRow) {
                /* Currently editing - but not this row - restore the old before continuing to edit mode */
                restoreRow(oTable, nEditing);
                editRow(oTable, nRow);
                nEditing = nRow;
            } else if (nEditing == nRow && this.innerHTML == "Save") {
                /* Editing this row and want to save it */
				//console.log(nEditing);
				var validated = validateInput(nEditing)
				
				if(validated.success){
					saveRow(oTable, nEditing);
					nEditing = null;
				}else{
					console.log(validated.error)
				}
				
                //alert("Updated! Do not forget to do some ajax to sync with backend :)");
            } else {
                /* No edit in progress - let's start one */
                editRow(oTable, nRow);
                nEditing = nRow;
            }
        });
    }

    return {

        //main function to initiate the module
        init: function () {
            handleTable();
        }

    };

}();