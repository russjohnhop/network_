document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('#edit').forEach(e =>e.addEventListener('click', function(event) {
        event.preventDefault();
        const editElement = event.target;
        const post_id = editElement.dataset.id;
        edit(post_id);
      }));
    document.querySelectorAll('.btn.btn-primary').forEach(e =>e.addEventListener('click', function(event) {
        event.preventDefault();
        const submit = event.target;
        const post_id = submit.dataset.id;
        save_post(post_id);
    }))
    document.querySelectorAll('.btn.btn-info').forEach(e =>e.addEventListener('click', function(event) {
        event.preventDefault();
        const likeBtn = event.target;
        const post_id = likeBtn.dataset.id ;
        console.log(post_id);
        like(post_id);
      }));
})


function edit(post_id) {
    console.log("post_id = " + post_id)

// Fetch post data
fetch(`/posts/${post_id}`)
.then(response => response.json())
.then(post => {

//     When a user clicks “Edit” for one of their own posts, the content of their post should be replaced with a textarea where the user can edit the content of their post.
    
// Write code here to select the correct post-block
    const parentPost = `post${post_id}`
    const postParent = document.querySelector(parentPost)


// Rewrite all of the below to use the parent to select the right element

// Select existing post content
    // const postContent = document.querySelector('#post-content');
    const postContent = document.querySelector('#post-content' + post_id);

    // Create textarea
    let textarea = document.createElement('textarea');

    console.log("textarea = " + postContent)
    textarea.textContent = postContent.textContent
    console.log("textarea value = " + textarea.value)
    textarea.id = `new-content${post_id}`

    // Hide the uneditable post
    postContent.style.display = "none";

    // Get parent element to append to
    const parentElement = document.querySelector('#edit-form' + post_id);
    console.log("parentElement = " + parentElement);

    // Append textarea to the card/editform
    parentElement.appendChild(textarea)

    // Display submit btn
    submitBtn = document.querySelector('#submit-btn' + post_id)
    submitBtn.style.display = "inline";

//     The user should then be able to “Save” the edited post. Using JavaScript, you should be able to achieve this without requiring a reload of the entire page.
// For security, ensure that your application is designed such that it is not possible for a user, via any route, to edit another user’s posts.

})}

//     The user should then be able to “Save” the edited post. Using JavaScript, you should be able to achieve this without requiring a reload of the entire page.

function save_post(post_id) {
    const new_post_content = document.querySelector('#new-content' + post_id);
    const postContent = document.querySelector('#post-content' + post_id);


        fetch(`/posts/${post_id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            post_content:new_post_content.value
        })
    })
    // Display post data (populate text area)
        postContent.textContent = new_post_content.value;

    // Display old text block

    postContent.style.display = "inline";

    // Hide submit button

    submitBtn = document.querySelector('#submit-btn' + post_id)
    submitBtn.style.display = "none";

    // Hide text area

    new_post_content.style.display = "none" ;

}

    function getCookie(name) {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1);
          }
        }
        return '';
      }



function like(post_id){

fetch(`/posts/like/${post_id}`) 
.then(response => response.json())
.then(post => {
    // Select count element
    console.log("post_id = " + post_id)
    const likeId = `likeCount${post_id}`
    let likeCount = document.querySelector(`#${likeId}`);
    console.log("likeCount =" + likeCount)
    // Below is undefined
    const postLikes = post.likes_count ?? 0;
    console.log("postLikes = " + postLikes)

    // Update the element based on the likes on the post

    likeCount.textContent = postLikes;
    console.log("likeCount.textContent = " + postLikes)

    // Select the Like button
    const likeBtnId = `like-btn${post_id}`

    const likeBtn = document.querySelector(`#${likeBtnId}`);

    // Change text on button depending on current text

    if (likeBtn.textContent == "Like" ) {
        likeBtn.textContent = "Unlike"
    }
    else if (likeBtn.textContent == "Unlike") {
        likeBtn.textContent = "Like"
    }

  })}


