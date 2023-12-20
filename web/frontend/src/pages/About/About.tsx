import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import styles from './About.module.css'

interface highlightProps {
  highlightedParagraph: string | null;
  highlight : (id: string | null) => void;
}

const About: React.FC<highlightProps> = ({highlightedParagraph, highlight}) => {
    console.log(highlightedParagraph)

    useEffect(() => {
        const divs = document.querySelectorAll('div');
        divs.forEach((div) => {
          if (div.id === highlightedParagraph) {
            div.classList.add(styles.highlighted);
          }
          else {
             div.classList.remove(styles.highlighted);
          }
        });

        // Remove highlight after 5 seconds
            const timeoutId = setTimeout(() => {
              divs.forEach((div) => {
               if (div.id === highlightedParagraph) {
                    div.classList.remove(styles.highlighted);
                }
              });
              highlight(null);
            }, 500);

            return () => clearTimeout(timeoutId);
      }, [highlightedParagraph]);

      useEffect(() => {
          // Additional effect to handle the initial rendering when highlightedParagraph is null
          const divs = document.querySelectorAll('div');
          divs.forEach((div) => {
            div.classList.remove(styles.highlighted);
          });
        }, []); // Empty dependency array for initial rendering

    return (
        <div className={styles.PageContent}>
        <article>
            <p><Link to="/">Back to Main Page</Link></p>
            <h2 className={styles.AboutHeader}>About</h2>
            <div id="" className={styles.contents}><p className={styles.AboutContent}>
                    Piro is an application that assists with rational planning of solid-state synthesis routes for inorganics.
                    It is a recommendation system for navigation and planning of synthesis of inorganic materials based on classical
                    nucleation theory and semi-empirical, data-driven approximations to its parts. Currently it works with Materials Project data via its Rester API.
                    <br/><br/>
                    Piro creates synthesis reaction planning plots for target polymorphs under a specific set of thermodynamic
                    conditions and a precursor library, where favorable routes are those that are (nearly) Pareto optimal in terms of two metrics:
                    nucleation barrier and phase-selection. It allows retrosynthetic analysis of target inorganic materials
                    to generate a synthesis reaction tree. (i.e. laying out the reaction pathways necessary to arrive at the
                    target from practical/purchasable reagents/starting materials)
            </p></div>
            <div id="contact" className={styles.contents}><h4 className={styles.Titles}>Contact</h4>
            <p className={styles.TitlesContent}>
                    The piro platform is developed by a team of researchers and software developers at Toyota Research Institute: Murat Aykol,
                    Joseph Montoya, Jens Hummelshøj, Chris Fajardo, Michael Puzon, and Reko Ong.
                    If you have any questions or feedback, please reach out to us at <a href="mailto:em-piro@tri.global">em-piro@tri.global</a>
            </p></div>
            <div id="code" className={styles.contents}><h4 className={styles.Titles}>Code</h4>
            <p className={styles.TitlesContent}>
                    If you’d like to use the python interface to piro, or to access the code for this site,
                    please visit our github page: <a href="https://github.com/TRI-AMDD/piro" target="_blank">https://github.com/TRI-AMDD/piro</a>.
                    Tutorial jupyter notebooks showing how to use piro locally are provided in the notebooks folder.
            </p>
            </div>
            <div id="manuscript" className={styles.contents}>
            <h4 className={styles.Titles}>Manuscript</h4>
            <p className={styles.TitlesContent}>
                    For more information about the physical theory behind piro, please read our paper,
                    “Rational Solid-State Synthesis Routes for Inorganic Materials” by Murat Aykol et al.
                    <a href="https://pubs.acs.org/doi/abs/10.1021/jacs.1c04888" target="_blank">(https://pubs.acs.org/doi/abs/10.1021/jacs.1c04888)</a>.
            </p></div>
        </article>
        </div>
    );
};

export default About;