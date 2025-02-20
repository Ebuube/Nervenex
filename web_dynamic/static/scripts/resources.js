#!/usr/bin/node
//properties of the resource page
$(function () {
    //select the actice tab
    function filterTabs() {
        $('.tabs .hyperlink').click(function() {
            $('.tabs .hyperlink').removeClass('active');
            $(this).addClass('active');
        // show or hide resources based on selected tab
            var tab = $(this).text().toLowerCase();
            $('.flex_list_item').hide();
            $('.' + tab).show();
        });
    };
    filterTabs()
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
                position: "top-end",
                icon:'error',
                title: 'Oops...🥲',
                text: 'Please fill in all required fields😊. ',
                timer: 1500
    
        
        });
        return;
        }
      
        // Send data to API - Not working
        $.ajax({
          url: `${API_BASE_URL}/resources`,
          type: "POST",
          data : JSON.stringify({
            title: title,
            description: description,
            link: link,
            type: type
          }),
          contentType: "application/json",
          success: function(data) {
            Swal.fire({
                position: "top-end",
                icon: "success", 
                title: "Resource uploaded successfully!",
                text: "Your resource is now available to others.",
                showConfirmButton: false,
                timer: 1500
            });
            //getAllResources(); // Update resources list(func not written)
          },
          error: function(error) {
            console.error(error);
            alert("Error uploading resource. Please try again.");
          }
        });
      }
      
      // Bind submit button click
      $("#upload_resource button.submit").click(function() {
        submitUploadForm();
      });



});

    
    
    








