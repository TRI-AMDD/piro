import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import styles from './About.module.css';
import chevron_left from '../../images/chevron-left.png';

interface highlightProps {
  highlightedParagraph: string | null;
  highlight: (id: string | null) => void;
}

const About: React.FC<highlightProps> = ({ highlightedParagraph, highlight }) => {
  useEffect(() => {
    const divs = document.querySelectorAll('div');
    divs.forEach((div) => {
      if (div.id === highlightedParagraph) {
        div.classList.add(styles.highlighted);
      } else {
        div.classList.remove(styles.highlighted);
      }
    });

    // Remove highlight after 5 seconds
    setTimeout(() => {
      divs.forEach((div) => {
        if (div.id === highlightedParagraph) {
          highlight(null);
          div.classList.remove(styles.highlighted);
        }
      });
    }, 4000);

    return () => {
      divs.forEach((div) => {
        if (div.id === highlightedParagraph) {
          highlight(null);
          div.classList.remove(styles.highlighted);
        }
      });
    };
  }, [highlightedParagraph, highlight]);

  return (
    <div className={styles.PageContent}>
      <article>
        <p style={{ display: 'flex', alignItems: 'center' }}>
          <Link to="/">
            <img src={chevron_left} alt="chevron-left" width={'20px'} height={'20px'} />
          </Link>
          <Link to="/" className={styles.Breadcrumbs}>
            Back to Main Page
          </Link>
        </p>
        <h2 className={styles.AboutHeader}>About</h2>
        <div id="">
          <div className={styles.InnerContainer}>
            <p className={styles.Content}>
              Piro is an application that assists with rational planning of solid-state synthesis routes for inorganics.
              It is a recommendation system for navigation and planning of synthesis of inorganic materials based on
              classical nucleation theory and semi-empirical, data-driven approximations to its parts. Currently it
              works with Materials Project data via its Rester API.
              <br />
              <br />
              Piro creates synthesis reaction planning plots for target polymorphs under a specific set of thermodynamic
              conditions and a precursor library, where favorable routes are those that are (nearly) Pareto optimal in
              terms of two metrics: nucleation barrier and phase-selection. It allows retrosynthetic analysis of target
              inorganic materials to generate a synthesis reaction tree (i.e., laying out the reaction pathways
              necessary to arrive at the target from practical/purchasable reagents/starting materials).
            </p>
          </div>
        </div>
        <p className={styles.gap}></p>
        <div id="contact">
          <div className={styles.InnerContainer}>
            <h4 className={styles.Titles}>Contact</h4>
            <p className={styles.Content}>
              The Piro platform is developed by a team of researchers and software developers at Toyota Research
              Institute: Murat Aykol, Joseph Montoya, Jens Hummelshøj, Chris Fajardo, Michael Puzon, and Reko Ong. If
              you have any questions or feedback, please reach out to us at{' '}
              <u>
                <a href="mailto:em-piro@tri.global" className={styles.mailstyle}>
                  em-piro@tri.global
                </a>
              </u>
              .
            </p>
          </div>
        </div>
        <p className={styles.gap}></p>
        <div id="code">
          <div className={styles.InnerContainer}>
            <h4 className={styles.Titles}>Code</h4>
            <p className={styles.Content}>
              If you’d like to use the Python interface to Piro, or to access the code for this site, please visit our
              GitHub page:{' '}
              <u>
                <a href="https://github.com/TRI-AMDD/piro" target="_blank" rel="noreferrer">
                  https://github.com/TRI-AMDD/piro
                </a>
              </u>
              . Tutorial Jupyter notebooks showing how to use Piro locally are provided in the <a href="https://github.com/TRI-AMDD/piro/tree/main/piro/notebooks" target="_blank" rel="noreferrer">
                  <u>notebooks folder</u>
                </a>.
              <div className={styles.spacer}></div>
            </p>
          </div>
        </div>
        <p className={styles.gap}></p>
        <div id="manuscript">
          <div className={styles.InnerContainer}>
            <h4 className={styles.Titles}>Manuscript</h4>
            <p className={styles.Content}>
              For more information about the physical theory behind Piro, please read our paper, “Rational Solid-State
              Synthesis Routes for Inorganic Materials” by Murat Aykol et al.{' '}
              <u>
                <a href="https://pubs.acs.org/doi/abs/10.1021/jacs.1c04888" target="_blank" rel="noreferrer">
                  (https://pubs.acs.org/doi/abs/10.1021/jacs.1c04888)
                </a>
              </u>
              .<div className={styles.spacer}></div>
            </p>
          </div>
        </div>
      </article>
    </div>
  );
};

export default About;
