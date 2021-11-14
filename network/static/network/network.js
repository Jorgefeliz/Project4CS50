document.addEventListener('DOMContentLoaded', function() {

    
  

  });

  function add_follower(user_id){
    console.log(user_id);
    let route = "/followers/" + user_id ; 
    console.log(route);
    fetch(route, {
        method: 'POST',
        body: JSON.stringify({
            user_id: user_id
            
        })
      })
      .then(response => response.json())
      .then(result => {
          // Print result
 
          console.log(result);
      });
    localStorage.clear();
  }


function edit_post(comment_id){

  let mydiv = "#post" + comment_id;
  let route = '/edit_post' 

  console.log(route)
  fetch(route, {
    method: 'POST',
    body: JSON.stringify({
        comment_id: comment_id
  
           })
      })
  .then(response => response.json())
  .then(result => {
      // Print result
 
      console.log(result);
       
  document.querySelector(mydiv).innerHTML = `
  <div class="posting" id="post${comment_id}">
     

  <textarea> ${result["comment"]} </textarea>

  <button type="button" class="btn btn-primary btn-sm">Post </button>
  <br>

  
     <hr>
  </div>
  `;

        });

  //alert("Your trying to edit" + comment_id)


}
  