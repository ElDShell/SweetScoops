document.addEventListener("DOMContentLoaded",function(){
    const filterLinks = document.querySelectorAll("#portfolio-flters a");
    filterLinks.forEach((link) =>{
        link.addEventListener("click",function (event){
            event.preventDefault()
            const url =this.href;

            fetch(url,{
                headers: { "X-Requested-With": "XMLHttpRequest" },
            })
            .then((response) => response.json())
            .then((data)=>{
                const gallery = document.getElementById("gallery-container");
                gallery.innerHTML = "";

                data.products.forEach((product)=>{
                    const div = document.createElement("div");
                    div.classList.add("col-lg-4","col-md-6","p-0","portfolio-item")
                    div.innerHTML = `
                    <div class="position-relative overflow-hidden">
                        <img class="img-fluid w-100 fixed-size" src="${product.img_url}" alt="">
                        <a class="portfolio-btn overlay" href="${product.img_url}" data-lightbox="portfolio">
                            <i class="fa fa-plus text-primary" style="font-size: 60px;"></i>
                        </a>
                    </div>
                `;
                gallery.appendChild(div);
                });
                // adjustFooterPosition()
                const prevButton = document.querySelector("#prev-button");
                const nextButton = document.querySelector("#next-button");

                if (data.has_previous){
                    prevButton.style.display = 'inline-block';
                    prevButton.href = `?flavor=${data.flavor}&page=${data.previous_page_number}`;

                }else{
                    prevButton.style.display = 'none';
                }
                if  (data.has_next){
                    nextButton.style.display = 'inline-block';
                    nextButton.href =`?flavor=${data.flavor}&page=${data.next_page_number}`;
                }else{
                    nextButton.style.display = 'none';
                }

            })
            .catch((error) => console.error("Error",error));
        });

    });

    // Function to adjust footer position
    // function adjustFooterPosition() {
    //     // Check if the content's height has changed and adjust the footer accordingly
    //     const body = document.body;
    //     const html = document.documentElement;
    //     const footer = document.getElementById("footer");
    
    //     const height = Math.max( body.scrollHeight, body.offsetHeight, 
    //                              html.clientHeight, html.scrollHeight, html.offsetHeight );
    
    //     footer.style.position = (height <= window.innerHeight) ? 'absolute' : 'relative';
    // }

});
