
document.addEventListener("DOMContentLoaded", function () {

    // Get the chapter index navigation element
    const chapter_index = document.getElementById("chapter-index");

    // Get all headers with the class 'sectionlink'
    const headers = document.getElementsByClassName("sectionlink");

    // Create a doc fragment to add all the content
    const fragment = document.createDocumentFragment()

    for (const header of headers) {
        // Create a new id for each header based on its content
        const id = header.textContent.trim().toLowerCase().replace(/[:()/¿?áéíóú]/g, "").replace(/ /g, "-");
        header.id = id;

        // Create a new link element
        var link = document.createElement("a");
        link.href = "#" + id;
        link.textContent = header.textContent;
        link.className = "nav-link";

        //append the link to the fragment
        fragment.appendChild(link)
    }

    //append the fragment to the index
    chapter_index.appendChild(fragment)
});