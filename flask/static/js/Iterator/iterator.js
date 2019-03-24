$(document).ready(function() {
	
	UploadIterator.receivedText = UploadIterator.receivedText.bind(UploadIterator)
	UploadIterator.receivedText = function() {
		var data = (JSON.parse(self.fr.result));
		if(!Upload.validateJSON("iterator", data)) {
			return;
		}
		console.log(data);
		
		jQuery("#stateNameWrapper > div > div:nth-child(5) > div:nth-child(2) > div > input").val(data.container_name)
		jQuery("#customContent > div > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(5) > div:nth-child(2) > div > input").val(data.iterator_name)
		
		data.supported_types.forEach(function(type, i) {
			jQuery("#funcDeclDivRow > div > div > div > div > div:nth-child("+(i+1)+") > div > button.btn.btn-outline-secondary.addParameterBtn").first().trigger("click");
			jQuery("#funcDeclDivRow > div > div > div > div > div:nth-child("+(i+1)+") > input").val(type)
		});
		
		jQuery("#funcDeclDivRow > div > div > div > div > div:last-child > div > button.btn.btn-outline-secondary.delParameterBtn").first().trigger("click");
		
		Upload.validate();
	}

	UploadIterator.handleFileSelect = UploadIterator.handleFileSelect.bind(UploadIterator)
	$("#fileinput").change(UploadIterator.handleFileSelect);
	
    // START: Add a paramter functionality.
    $("#funcDeclWrapperRow").on('click', '.addParameterBtn', function(event) {
        console.log("addParameterTypeBtn");
        var eleToBeAddedTo = $(this).parents(".paramDiv");
        eleToBeAddedTo.append("\
            <div class='input-group repeatableParamListGroup'>\
                <input type='text' class='form-control validName paramType' placeholder='Data Type' aria-label='Parameter Type' aria-describedby='basic-addon2'\
                             tabindex='0' data-toggle='popover' data-trigger='manual' data-placement='left' data-content='Invalid Name'>\
                <div class='input-group-append'>\
                    <button class='btn btn-outline-secondary addParameterBtn' type='button' data-toggle='tooltip' data-placement='top' title='Add another parameter'>+</button>\
                    <button class='btn btn-outline-secondary delParameterBtn' type='button' data-toggle='tooltip' data-placement='top' title='Delete this parameter'>-</button>\
                </div>\
            </div>\
        ");
    });
    // END: Add a paramter functionality.

    // START: Delete a paramter functionality.
    $("#funcDeclWrapperRow").on('click', '.delParameterBtn', function(event) {
        // console.log("delParameterTypeBtn");
        var eleToBeDeleted = $(this).parents(".repeatableParamListGroup");
        // console.log(eleToBeDeleted);
        eleToBeDeleted.remove();        
    });
    // END: Delete a paramter functionality.

    // START: Cosmetic change to display file type selected in the dropdown.
    $(".fileType").on('click', function(event) {
        $("#fileTypeBtn").text($(this).text());
    });
    // END: Cosmetic change to display file type selected in the dropdown.

    // START : Code Download Functionality (includes form submission without forms per se)
    var errorNumber = 0;
    $("#codeDownload").on('click', function(event) {
        
        var errorCheckAttributes={
            isErraneousForm:false
        };

        function checkPopover(fn) {
            function inner(scope,type) {
                var ele = scope.find(type);
                if(ele.attr('isValidInput')=="true"){
                    return fn(ele);
                }
                else{
                    errorCheckAttributes["isErraneousForm"] = true;
                    ele.popover('show');
                }
            }
            return inner
        };


        // Step 1: Get All variables (haha, seems so simple :) )

        function getParamTypesList(scope) {
            var paramTypeList = [];
            var curParamTypeChildren = scope.find('.paramType');
            curParamTypeChildren.each(function(index, el) {
                if($(this).attr('isValidInput')=="true"){
                    paramTypeList.push($(this).val());
                }
                else{
                    errorCheckAttributes["isErraneousForm"] = true;
                    $(this).popover('show');
                }
            });
            return paramTypeList;
        }
        
        function getParamNamesList(scope) {
            var paramNameList = [];
            var curParamNameChildren = scope.find('.paramName');
            curParamNameChildren.each(function(index, el) {
                if($(this).attr('isValidInput')=="true"){
                    paramNameList.push($(this).val());
                }
                else{
                    errorCheckAttributes["isErraneousForm"] = true;
                    $(this).popover('show');
                }
            });
            return paramNameList;
        }

        function getFuncName(ele,type) {
            return ele.val();
        }

        function getFuncRetType(ele,type) {
            return ele.val();
        }

        function getContainer(){
			var name = ""
            $(".containerName").each(function(index, el) {
                if($(this).attr('isValidInput')=="true"){
					console.log($(this).val())
                    name = $(this).val()
                }
                else{
                    errorCheckAttributes["isErraneousForm"] = true;
                    $(this).popover('show');
                }
            });
			return name
        }
		
		function getIterator(){
			var name = ""
            $(".iteratorName").each(function(index, el) {
                if($(this).attr('isValidInput')=="true"){
                    name = $(this).val()
                }
                else{
                    errorCheckAttributes["isErraneousForm"] = true;
                    $(this).popover('show');
                }
            });
			return name
        }

        function getFunctionDeclList() {
            // repeatableFuncDeclList
            var functionsList = [];
            $(".repeatableFuncDeclList").each(function(index, el) {
                functionsList.push({
                    "name":getFuncName($(this),".funcName"),
                    "param_types":getParamTypesList($(this)),
                    "param_names":getParamNamesList($(this)),
                    "return":getFuncRetType($(this),".retTypeName")
                });
            });
            return functionsList;
        }

        getFuncName = checkPopover(getFuncName);
        getFuncRetType = checkPopover(getFuncRetType);

        var inpData = {
            "pattern":"iterator",
            "container_name":getContainer(),
            "iterator_name":getIterator(),
            "supported_types":getParamTypesList($(".repeatableFuncDeclList")),
            "fileType":$("#fileTypeBtn").text(), //this key will be removed in backend.
        }
        console.log("inpData:",inpData)
        if(!errorCheckAttributes["isErraneousForm"]){
            // do AJAX POST and send it away, woo
            console.log(inpData);

            $.ajax({
                url: "commonCodeCreate",
                type: "POST",
                dataType: "JSON",
                data: JSON.stringify(inpData),
                contentType:"application/json; charset=UTF-8"
            })
            .done(function(info) {
                console.log("success");
                console.log("success info:",info);
                if(info["success"]==1)
                {
                    $("#downloadCodeForm").submit(); //download the code. AJAX can't download by itself
                }
            })
            .fail(function(info) {
                console.log("error");
                console.log("error info:",info);
            })
            .always(function() {
                console.log("complete");
                console.log("complete info:",$(this));
            });
            
        }
        else{
            if(errorNumber<2){
                $("#errorModal").on('show.bs.modal', function(event) {
                    $("#errorModalBody").text("Check and correct the inputs which are being pointed to.Whenever you are ready, click Download again.");
                });
                $("#errorModal").modal("toggle");
            }
            else if(errorNumber<4){
                $("#errorModal").on('show.bs.modal', function(event) {
                    $("#errorModalBody").text("Correct the inputs which are being pointed to.");
                });
                $("#errorModal").modal("toggle");
            }
            else{
                $("#errorModal").on('show.bs.modal', function(event) {
                    $("#errorModalBody").text("Ok now, read the entries and enter properly.");
                });
                $("#errorModal").modal("toggle");
            }
            errorNumber++;
            console.log(errorNumber);
        }
    });

    // END : Code Download Functionality (includes form submission without forms per se)
    
    // START : State name validation
    function matchExact(r, str) {
       var match = str.match(r);
       return match != null && str == match[0];
    }
    $(".entireStateWrapper").on("focus",".validName", function(event) {
        $(this).popover("hide");
    });

    $(".entireStateWrapper").on("input",".validName", function(event) {
        // data-toggle="tooltip" data-placement="left" title="Tooltip on top"

        var res;
        
        res = matchExact(/[A-Za-z_]+[A-Za-z0-9_]*/g,$(this).val()); //basically it's a valid variable in a language like C++
        
        if($(this).hasClass("retTypeName") || $(this).hasClass("paramType"))
        {
            res = matchExact(/([A-Za-z_]+[A-Za-z0-9_]*)[\&\*]*/g,$(this).val()); //basically it's a valid variable in a language like C++
        }

        if(res==false){
            console.log("here");
            $(this).attr("isValidInput",false);
            $(this).css('color', 'red');
        }
        else{
            $(this).attr("isValidInput",true);
            $(this).css('color', 'green');
        }
    });

    $(".entireStateWrapper").on("focus",".validName", function(event) {
        if($(this).attr("isValidInput") == "true"){
            $(this).css('color', 'green');
        }
        else
        {
            $(this).css('color', 'red');
        }
    });

    $(".entireStateWrapper").on("blur",".validName", function(event) {
        if($(this).attr("isValidInput") == "true"){
            $(this).css('color', 'black');
        }
    });
    // END : State name validation

});