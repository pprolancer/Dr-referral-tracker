'use strict';

/*MetronicApp.controller('WithAjaxCtrl',  WithAjaxCtrl);



function WithAjaxCtrl(DTOptionsBuilder, DTColumnBuilder) {
    var vm = this;
	
    vm.dtOptions = DTOptionsBuilder.fromSource('json/org_data.json')
        .withPaginationType('full_numbers');
    vm.dtColumns = [
        DTColumnBuilder.newColumn('id').withTitle('ID'),
		DTColumnBuilder.newColumn('org_name').withTitle('Name'),
        DTColumnBuilder.newColumn('org_contact_name').withTitle('Contact Name'),
        
		DTColumnBuilder.newColumn('org_phone').withTitle('User Name'),
		DTColumnBuilder.newColumn('org_email').withTitle('User Name'),
		DTColumnBuilder.newColumn('org_special').withTitle('User Name')
    ];
}
*/



MetronicApp.controller('OrganizationsController', function($rootScope, $scope, $timeout, orgData, orgDataService,$q, $route ) {
    $scope.$on('$viewContentLoaded', function() {   
       // initialize core components
       // Metronic.initAjax();
			//$(document).ready(function(e) {
		
        	// init demo features
			////Demo.init()
			
    //});
    });
	$scope.orgData  = orgData;
	
	
	
	$scope.modalData = {}
	$scope.errorData = {}
	$scope.postRequestType = false
	$scope.putRequestType = false
	
	
	//// HTML page click handlers//////////////////
	$scope.handleCreateNewOrgClick =function(){
		//alert("in")
		$scope.postRequestType = true
		$scope.putRequestType = false
		$("#orgModal").modal('show');
		
	}
	
	$scope.handleEditClick=function($event , data){
		$scope.postRequestType = false;
		$scope.putRequestType = true;
		
		$scope.modalData = $scope.createCloneObj(data);
		$("#orgModal").modal('show');
		console.log("handleEditClick", $scope.modalData)
	}
	$scope.handleDeleteClick=function($event , data){
		
		orgDataService.deleteData(data, $scope.handleSuccessDelete, $scope.handleError);
		//$scope.modalData = $scope.createCloneObj(data);
		//$("#orgModal").modal('show');
		console.log("handleEditClick", $scope.modalData);
	}
	//////////////////
	
	//////Modal event Handlers/////////////
	$scope.closeModal = function(){
		
		console.log("closeModal")
		$scope.errorData = {}
		$scope.modalData = {}
		$("#orgModal").modal('hide');
		
	}
	
    $scope.resetModal=function(){
		
		console.log("resetModal")
		$scope.errorData = {}
		$scope.modalData = {}
		
	}
	
    $scope.submitModalPost=function(data){
		
		orgDataService.saveData(data, $scope.handleSuccessPost, $scope.handleError)
		
	}
	
	$scope.submitModalPut=function(data){
		
		orgDataService.editData(data, $scope.handleSuccessPut, $scope.handleError)
		
	}
	
	
	////////////////////////
	
	//////Server responce Handler///////////
	$scope.handleSuccessPut = function(res,_data){
		
		console.log("handleSuccess", res)
		for(var i in $scope.orgData.results){
			if($scope.orgData.results[i].id === $scope.modalData.id){
				for(var a in $scope.orgData.results[i]){
					$scope.orgData.results[i][a]  = $scope.modalData[a]
				}
			}
		}
		$scope.closeModal()
	}
	$scope.handleSuccessPost=function(res,_data){
		
		console.log("handleSuccess", res)
		$scope.orgData.results.push(_data)
		$scope.getOrgData()
		$scope.closeModal()
	}
	
	$scope.handleSuccessDelete=function(res,_data){
		
		console.log("handleSuccess", res)
		$scope.getOrgData();
		
	}
	
	$scope.handleError=function(res){
		
		console.log("handleError", res)
		$scope.errorData = res.data
		console.log($scope.errorData)
	}
	///////////////
	
	////
	 $scope.getOrgData = function(){
		var deferred = $q.defer();
		orgDataService.getData()
		.then(function(event){
			deferred.resolve(event);
			console.log("appjs",event);
			$scope.orgData = event
		});
		
		//$scope.orgData  =  deferred.promise
	}

	
	
	$scope.createCloneObj=function(data){
		var obj={}
		for(var a in data){
			obj[a] = data[a]
		}
		return obj;
	}
	
	
	////Modal Form validation//////////////
	$scope.validateForm = function(formElement){
			//console.log(formElement);
			
			$(formElement).validate({
				invalidHandler: function(form, validator) {
					//alert('invalidHandler');
					//return false
				},
				success: function(label) {
					//alert('succes:' + label);
					//return false
				},
				submitHandler: function(form) {
				// some other code
				// maybe disabling submit button
				// then:
					console.log("validateForm",$scope.modalData)
					if($scope.postRequestType){
						
						$scope.submitModalPost($scope.modalData)
						
					}else{
						
						$scope.submitModalPut($scope.modalData)
					}
				//$(form).submit();
			  },
				rule:{
					
					id:{
      					number: true	
					},
					orgName:{
						required: true,
      					maxlength: 254	
					},
					orgType:{
						required: true
					},
					orgContactName:{
      					maxlength: 254	
					},
					orgPhone:{
						phoneUS: true
					},
					orgEmail:{
						 email: true	
					},
					orgSpecial:{
						
					}

				},
				messages:{
					id:{
						required: "Please provide ID.",
      					number: "Id should contain only number."	
					},
					orgName:{
						required: "Please provide the Organization Name.",
      					maxlength: "Organization Name should not exceed 254 charactors. "	
					},
					orgType:{
						required: "Please Select the Organization Type."
					},
					orgContactName:{
						required: "Please provide the Organization Contact Name.",
      					maxlength: "Organization Contact Name should not exceed 254 charactors. "	
					},
					orgPhone:{
						phoneUS: "Enter a valied Phone Number."
					},
					orgEmail:{
						 email: "please enter a valied email adress."	
					},
					orgSpecial:{
						
					}
				}
			})
			
		}
		
		
	/////
	
	$timeout(function() {
		
		$scope.validateForm($("#orgCreaterForm"))
		 $('#orgTable').DataTable( {
        	"pagingType": "full_numbers",
			"lengthMenu": [
                [5, 15, 20, -1],
                [5, 15, 20, "All"] // change per page values here
            ],
			"pageLength": 5,
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
   		 } );
		//TableEditable.init(); 
	},0);
	
	
	/*$("#orgCreaterFor").click(function(){
		
		var event = {
			"id": "8",
			"creation_time": "02/02/2016",
			"modification_time": "02/02/2016",
			"org_name": "Lava ORG",
			"org_type": "",
			"org_contact_name": "LAVA",
			"org_phone": "",
			"org_email": "kusha.w@gmail.com",
			"org_special": false,
			"clinic": "3"
		}
		orgDataService.editData(event)
		
	});*/
	
	
	//console.log($scope.orgData)
	/*$http.get('../../api/v1/organization/')
       .then(function(res){
          $scope.orgData = res.data;
		  //console.log($scope.orgData) 
		  $timeout(function() {
			    //console.log("TableEditable.init - initiated _1")
				
				
			},0);
        });*/
	


    // set sidebar closed and body solid layout mode
    $rootScope.settings.layout.pageSidebarClosed = false;
});