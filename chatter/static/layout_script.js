// Javascript for layout

// Remove the username from LocalStorage
logout_btn = () => {
	localStorage.removeItem("username");
	location.reload();
}