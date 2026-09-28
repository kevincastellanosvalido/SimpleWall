const postInput = document.querySelector(".postInput");
const postButton = document.querySelector(".submitButton");


// on click, gets what the user typed(removing leading spaces at the beginning and end), prints user's text in dev console
postButton.addEventListener("click", () =>{ 
    const text = postInput.value.trim();
    if(!text){ // checks whether there is text or not inside the postInput box
        return;
    }

    const newPost = document.createElement("div");
    const postContent = document.createElement("p");

    /* the block below will create a simple post(no buttons, just text). this will not be saved anywhere(yet) so it'll disappear on refresh.
       will only be visible by user clicking on post.*/
    newPost.classList.add("post");
    postContent.classList.add("postContent");
    postContent.textContent = text;
    newPost.appendChild(postContent);
    document.querySelector(".posts").prepend(newPost);

    console.log(text);
});