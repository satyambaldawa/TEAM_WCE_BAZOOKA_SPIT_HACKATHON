const body = document.querySelector("body");
const modal = document.querySelector(".modal");
const modal2 = document.querySelector(".modal2");
const modalButton = document.querySelector(".modal-button");
const modalButton2 = document.querySelector(".modal-button2");
const closeButton2= document.querySelector(".close-button2");

const closeButton = document.querySelector(".close-button");
let isOpened = false;

const openModal = () => {
  modal.classList.add("is-open");
  body.style.overflow = "hidden";
};

const closeModal = () => {
  modal.classList.remove("is-open");
  body.style.overflow = "initial";
};
const openModal2 = () => {
  modal2.classList.add("is-open");
  body.style.overflow = "hidden";
};

const closeModal2 = () => {
  modal2.classList.remove("is-open");
  body.style.overflow = "initial";
};


modalButton.addEventListener("click", openModal);
closeButton.addEventListener("click", closeModal);
modalButton2.addEventListener("click", openModal2);
closeButton2.addEventListener("click", closeModal2);

document.onkeydown = evt => {
  evt = evt || window.event;
  evt.keyCode === 27 ? closeModal() : false;
};