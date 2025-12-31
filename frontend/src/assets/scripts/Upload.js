// src/components/uploadHandler.js

export const handlePdfUpload = async (event, setFileName) => {
  const file = event.target.files[0];

  if (!file) return;

  // Check PDF file type
  if (file.type !== "application/pdf") {
    alert("Please upload a PDF file only!");
    return;
  }

  // Display file name
  setFileName(file.name);

  // Simulate upload process
  const formData = new FormData();
  formData.append("pdf", file);

  try {
    // Replace with your backend API
    const response = await fetch("http://localhost:5000/upload", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      alert("PDF uploaded successfully!");
    } else {
      alert("Upload failed. Try again.");
    }
  } catch (error) {
    console.error("Error uploading file:", error);
    alert("Something went wrong.");
  }
};
