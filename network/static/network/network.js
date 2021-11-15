document.addEventListener('DOMContentLoaded', function() {

    
  

  });

  function add_follower(user_id){
 
    let route = "/followers/" + user_id ; 

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

  let mydiv = "texto" + comment_id;

  let route = '/edit_post' 

  fetch(route, {
    method: 'POST',
    body: JSON.stringify({
        comment_id: comment_id
  
           })
      })
    .then(response => response.json())
    .then(result => {
        // Print result
  
        //console.log(result);
     
  
  document.getElementById(mydiv).innerHTML = `
  <div id="texto{{comment.id}}"> 

              
    <textarea id="text${comment_id}"> ${result["comment"]} </textarea>
    <br>

    <input type="button" value="Update" onclick="update_post(${comment_id})" />

    <input type="button" value="Cancel" onclick="old_post( ${comment_id})" />
    <br>

   
</div> `;

        });

  //alert("Your trying to edit" + comment_id)


}

function update_post(comment_id){
  
  let mydiv = "texto" + comment_id;
  let new_comment = "text" + comment_id;
  
  new_comment = document.getElementById(new_comment).value;

  let route = '/edit_post' 

  fetch(route, {
    method: 'PUT',
    body: JSON.stringify({
        new_comment: new_comment,
        comment_id: comment_id,

  
           })
      })
  .then(response => response.json())
  .then(result => {
  
 
      
      //document.getElementById(mydiv).innerHTML = "";
      document.getElementById(mydiv).innerHTML = `
      
      <div id="texto${comment_id}"> 

              
        <p>${result["comment"]}</p>
        <input type="button" class="btn btn-primary btn-sm" value="Like" onclick="like_post( ${comment_id} )" />

        <input type="button" class="btn btn-secondary btn-sm" value="Edit" onclick="edit_post( ${comment_id} )" />
        <br>                       
    

      
      </div>
      `;

    });
  //alert("Your trying to edit" + comment_id)


}

function old_post( comment_id){

  let old_text = "text"+ comment_id;
  old_text = document.getElementById(old_text).value;
  
  let mydiv = "texto" + comment_id;
  document.getElementById(mydiv).innerHTML = `
      
  <div id="texto${comment_id}"> 

          
    <p>${old_text}</p>
    <input type="button" class="btn btn-primary btn-sm" value="Like" onclick="like_post( ${comment_id} )" />

    <input type="button" class="btn btn-secondary btn-sm" value="Edit" onclick="edit_post( ${comment_id} )" />
    <br>                       


  
  </div>
  `;


}

function like_post( comment_id ){

  let route = '/like_post' 

  
  fetch(route, {
    method: 'POST',
    body: JSON.stringify({
        comment_id: comment_id
  
           })
      })
    .then(response => response.json())
    .then(result => {
        // Print result
  
      

        let mydiv = "like" + comment_id;
        document.getElementById(mydiv).innerText = result["likes"] + " likes"

      });
}
  