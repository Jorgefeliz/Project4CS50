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
  