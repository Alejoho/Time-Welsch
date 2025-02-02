// Populates the index of the chapters

document.addEventListener("DOMContentLoaded", function () {

    // Get the chapter index navigation element
    const chapter_index = document.getElementById("chapter-index");

    // Get all headers with the class 'sectionlink'
    const headers = document.getElementsByClassName("sectionlink");

    // Create a doc fragment to add all the content
    const fragment = document.createDocumentFragment()

    position = "p-0 my-2"

    for (const header of headers) {
        // Create a new id for each header based on its content
        const id = header.textContent.trim().toLowerCase().replace(/[:()/¿?áéíóú]/g, "").replace(/ /g, "-");
        header.id = id;

        // Create a new link element
        let link = document.createElement("a");
        link.href = "#" + id;
        link.textContent = header.textContent;

        // Differentiate the header, applied the required class and indent
        // and append it to the fragment
        if (header.tagName === "H1") {
            link.className = `navbar-brand ${position} text-wrap`;
            fragment.appendChild(link)
        }
        else if (header.tagName === "H2") {
            link.className = `nav-link ${position} text-wrap`;
            fragment.appendChild(link)
        }
        else if (header.tagName === "H3") {
            if (fragment.lastElementChild.tagName != "div") {
                const new_div = document.createElement("div")
                new_div.className = "ms-3"
                fragment.appendChild(new_div)
            }
            link.className = `nav-link ${position} text-wrap`;
            fragment.lastElementChild.appendChild(link)
        }
    }

    // Add a link for the navigation panel at the bottom
    let link = document.createElement("a");
    link.href = "#navigationPanel";
    link.textContent = "Panel de navegación";
    link.className = `nav-link ${position} text-wrap text-dark`;
    fragment.appendChild(link)

    // Append the fragment to the index
    chapter_index.appendChild(fragment)
});