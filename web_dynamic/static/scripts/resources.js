#!/usr/bin/node
//properties of the resource page
$(function () {
    //reset the upload details
    function resetUploadForm() {
        $("#upload_resource input").val("");
        $("#upload_resource textarea").val("");
    }
    $("#upload_resource button.reset").click(function() {
        resetUploadForm();
      });
    
    $('.search').on('input', function() {
        // filter search based on text
        var searchText = $(this).val().toLowerCase();
        $('.flex_list_item').each(function() {
            var resourceTitle = $(this).find('h2').text().toLowerCase();
            if (resourceTitle.includes(searchText)) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });

    function submitUploadForm() {
        // upload a resource
        var title = $("#upload_resource input[name='title']").val();
        var description = $("#upload_resource input[name='description']").val();
        var type = $("#upload_resource select[name='type']").val();
        var link = $("#upload_resource input[name='link']").val();
        
      
        // Validate required fields
        if (!title || !description || !type || !link) {
            Swal.fire({
                icon:'error',
                title: 'Oops...🥲',
                text: 'Please fill in all required fields😊. '
        
        });
        return;
        }
      
        // Send data to API
        $.ajax({
          url: 'http://localhost:5001/api/v1/resources',
          type: "POST",
          dataType: JSON.stringify({
            title: title,
            description: description,
            link: link,
            type: type
          }),
          
        });
      }
      
      
});

    
    
    








