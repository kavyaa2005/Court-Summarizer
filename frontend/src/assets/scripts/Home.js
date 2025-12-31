// // src/assets/scripts/Home.js
// import gsap from "gsap";
// import ScrollTrigger from "gsap/ScrollTrigger";

// export const initAnimations = () => {
//   gsap.registerPlugin(ScrollTrigger);

//   // Intro section fade-up
//   gsap.from(".intro-text", {
//     opacity: 0,
//     y: 50,
//     duration: 1.2,
//     ease: "power3.out",
//   });

//   // About section
//   gsap.from(".about", {
//     scrollTrigger: {
//       trigger: ".about",
//       start: "top 80%",
//     },
//     opacity: 0,
//     y: 100,
//     duration: 1.2,
//     ease: "power3.out",
//   });

//   // Features cards pop-in
//   gsap.from(".feature-card", {
//     scrollTrigger: {
//       trigger: ".features",
//       start: "top 80%",
//     },
//     opacity: 0,
//     y: 100,
//     stagger: 0.2,
//     duration: 1,
//     ease: "back.out(1.7)",
//   });

//   // How it works steps
//   gsap.from(".how-it-works li", {
//     scrollTrigger: {
//       trigger: ".how-it-works",
//       start: "top 80%",
//     },
//     opacity: 0,
//     x: -50,
//     stagger: 0.3,
//     duration: 1,
//     ease: "power2.out",
//   });

//   // CTA section zoom-in
//   gsap.from(".cta-section", {
//     scrollTrigger: {
//       trigger: ".cta-section",
//       start: "top 85%",
//     },
//     opacity: 0,
//     scale: 0.8,
//     duration: 1,
//     ease: "power3.out",
//   });

//   // Footer fade-in
//   gsap.from(".footer", {
//     scrollTrigger: {
//       trigger: ".footer",
//       start: "top 95%",
//     },
//     opacity: 0,
//     y: 50,
//     duration: 1,
//     ease: "power2.out",
//   });
// };
