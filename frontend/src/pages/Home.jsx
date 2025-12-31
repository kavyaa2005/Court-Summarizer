import React, { useState } from "react";
import Navbar from "../components/NavBar";
import Footer from "../components/Footer";
import UploadModal from "../pages/button/Upload";   // ✅ Import popup
import "../assets/styles/Home.css";
import "../assets/styles/Watermark.css";

const Home = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <>
      {/* Navbar always on top */}
      {/* <Navbar /> */}

      {/* Main Home Page */}
      <div className={`home ${isModalOpen ? "blurred-bg" : ""}`}>
        {/* Intro Section */}
        <section className="intro-section">
          <div className="intro-text">
            <h1>Court Summarizer</h1>
            <p>
              Our platform helps legal professionals, students, and researchers
              quickly understand lengthy court judgments by generating accurate and
              concise summaries.
            </p>

            {/* ✅ Popup instead of redirect */}
            <button className="cta-btn" onClick={() => setIsModalOpen(true)}>
              Try Summarizer
            </button>
          </div>
        </section>

        {/* About Section */}
        <section className="about">
          <h2>Simplifying Complex Court Judgments</h2>
          <p>
            Legal documents and court judgments are often lengthy, complex, and time-consuming 
            to interpret. The <strong>Court Summarizer</strong> leverages advanced 
            Artificial Intelligence (AI) techniques to analyze and condense judicial 
            documents into precise, easy-to-understand summaries. 
            <br /><br />
            This solution enhances efficiency for legal professionals, researchers, and 
            citizens by improving accessibility, reducing the effort required to review 
            case files, and ensuring quick comprehension of critical information.
          </p>
        </section>

        {/* Features Section */}
        <section className="features">
          <h2>Key Features</h2>
          <div className="feature-grid">
            <div className="feature-card">
              <h3>Upload Court Orders</h3>
              <p>Upload PDF or text documents of judgments with ease.</p>
            </div>
            <div className="feature-card">
              <h3>AI Summarization</h3>
              <p>Get accurate summaries highlighting the main points and legal reasoning.</p>
            </div>
            <div className="feature-card">
              <h3>Quick Access</h3>
              <p>Save time by instantly viewing concise case outcomes.</p>
            </div>
          </div>
        </section>

        {/* How it Works Section */}
        <section className="how-it-works">
          <h2>How It Works</h2>
          <ol>
            <li>Step 1: Upload a court order (PDF).</li>
            <li>Step 2: Our AI processes the content.</li>
            <li>Step 3: Receive a clear, concise summary instantly.</li>
          </ol>
        </section>

        {/* CTA Section */}
        <section className="cta-section">
          <h2>Start Simplifying Legal Texts Today!</h2>
          <button className="cta-btn" onClick={() => setIsModalOpen(true)}>
              Go To Summarizer
            </button>
        </section>
      </div>

      {/* ✅ Popup Modal */}
      <UploadModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
    </>
  );
};

export default Home;
