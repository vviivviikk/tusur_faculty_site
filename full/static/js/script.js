document.getElementById("facultyForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const response = await axios.post("/recommend", {
        liked_subjects: Array.from(document.getElementById("likedSubjects").selectedOptions)
            .map(opt => opt.value),
        interests: document.getElementById("interests").value
    });
    document.getElementById("results").innerHTML = 
        response.data.faculties.map(f => `<div>${f.name}</div>`).join("");
});