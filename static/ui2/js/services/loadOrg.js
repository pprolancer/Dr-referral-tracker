// JavaScript Document
'use strict';

MetronicApp.service("orgDataService", function($resource, $http, $q){

	var resource  = $resource("../../api/v1/organization/:id", {id:"@id"})

	return{
		getData:function(){
			
			var deferred = $q.defer();
			resource.get({},	
			function(event){
				deferred.resolve(event)
				//handleSuccess(event);
				
			},
			function(response){
				
				deferred.reject(response)
				//handleError(response);
			});
			
			return deferred.promise;
		},
		
		saveData: function(_data,success,fail){				
			console.log("saveData")
			var req = {
			 method: 'POST',
			 url: '../../api/v1/organization/',
			 data: _data
			}
			$http(req).then(function(res){
				
				success(res,_data)
			}, 
			function(res){
				
				fail(res)
			});
			
		},
		editData: function(_data,success,fail){				
			console.log("editData")
			var req = {
			 method: 'PUT',
			 url: '../../api/v1/organization/'+ _data.id+"/",
			 data: _data
			}
			$http(req).then(function(res){
				
				success(res,_data)
			}, 
			function(res){
				
				fail(res)
			});
			
		},
		deleteData: function(_data,_success,_fail){
			
				
		
			
			if (confirm('Are you sure you want to delete the Organization?')==true){
			$.ajax({
				url : '../../api/v1/organization/'+ _data.id+'/',
				type : "DELETE", // http method,
				data : _data, // data sent with the delete request
				success : function(res) {
					// hide the post
				  //$('#post-'+post_primary_key).hide(); // hide the post on success
				  console.log("delete Success: ", res);
				  _success(res, _data) 
				  
				},
	
				error : function(xhr,errmsg,err) {
					// Show an error
					//$('#results').html("<div class='alert-box alert radius' data-alert>"+
					//"Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
					console.log("error: ", xhr, errmsg, err); // provide a bit more info about the error to the console
					_fail(xhr,errmsg,err)
				}
			});
			} else {
				return false;
			}
		
		
		
		}
		
		
					
		
	}

	
});