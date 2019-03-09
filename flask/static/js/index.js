$(document).ready(function() {
    $('[data-toggle="tooltipupload"]').tooltip(); 
    function capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }
    var originalPatternSearchBoxWrapperColor = $("#patternSearchBoxWrapper").css("background-color");
    $("#patternSearchBoxWrapper").focusin(function(event) {
        $(this).css('background-color', '#FFFFFF');
    });
    $("#patternSearchBoxWrapper").focusout(function(event) {
        $(this).css('background-color', originalPatternSearchBoxWrapperColor);
    });



    var patternArr = [
        "abstractFactory",
        "adapter",
        "bridge",
        "builder",
        "chainOfResponsibility",
        "command",
        "composite",
        "decorator",
        "facade",
        "factory",
        "flyweight",
        "interpreter",
        "iterator",
        "mediator",
        "memento",
        "observer",
        "policy",
        "prototype",
        "proxy",
        "singleton",
        "state",
        "templateMethod",
        "visitor"
    ];
    var trie = SuffixTree.fromArray(patternArr);
    var allPatternEles = $(".patternDivCol");
    var allPatternEleNames = [];
    
    $(".patternDivCol").each(function(index, el) {
        allPatternEleNames.push($(this).attr("name"));
    }); 


    // console.log(allPatternEleNames);

    // console.log(allPatternEles);
    $("#patternSearchBox").on('input', function(event) {
        $(".patternDivCol").each(function(index, el) {
            $(this).css('display', 'none');;
        });         
        var res = trie.find($(this).val());
        if (res && res.length){ //if res is not null and is not empty
            var intersection = allPatternEleNames.filter(value => -1 !== res.indexOf(value));

            $.each(allPatternEleNames, function(outIndex, outVal) {
                $.each(intersection, function(inIndex, inVal) {
                    if(outVal == inVal)
                    {
                        $("[name='"+inVal+"']").css('display', 'block');
                    }
                });
            });
        }
    });

    //remove repeatableElement functinality
    $(".removeBtn").each(function(index, el) {
        $(this).on('click', function(event) {
            // console.log("Remove");
            console.log($(this).parentsUntil($("#mainContainer"),".repeatableElement"));
        });
    });
    //add repeatableElement functinality
    var i=2;
    $(".addBtn").each(function(index, el) {
        $(this).on('click', function(event) {
            $("#mainContainer").append("\
                    <div class='row repeatableElement' id='row"+i+"'>\
                        <div class='col-xl-1 col-lg-1 col-md-1 col-1'>\
                            <input class='form form-control' type='text' name='retType'>\
                        </div>\
                        <div class='col-xl-1 col-lg-1 col-md-1 col-1'>\
                            <input class='form form-control' type='text' name='funcName'>\
                        </div>\
                        <div class='col-xl-3 col-lg-3 col-md-3 col-3'>\
                            <input class='form form-control' type='text' name='paramTypeList'>\
                        </div>\
                        <div class='col-xl-3 col-lg-3 col-md-3 col-3'>\
                            <input class='form form-control' type='text' name='paramNameList'>\
                        </div>\
                        <div class='col-xl-2 col-lg-2 col-md-2 col-2'>\
                            <button class='btn btn-danger removeBtn' >Remove</button>\
                        </div>\
                    </div>"); 
            i++;
            //remove repeatableElement functinality
            $(".removeBtn").each(function(index, el) {
                $(this).on('click', function(event) {
                    // console.log("Remove");
                    $(this).parentsUntil($("#mainContainer"),".repeatableElement").remove();
                });
            });
        });
    });

    // START : Clear button functionality
    $("#searchClearBtn").on('click', function(event) {
        $("#patternSearchBox").val("");        
        $(".patternDivCol").each(function(index, el) {
            $(this).css('display', 'block');;
        }); 
    });
    // END : Clear button functionality
});