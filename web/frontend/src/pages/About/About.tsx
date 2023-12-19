import { Link } from 'react-router-dom';
import styles from './About.module.css'

export default function About() {
    return (
        <article className={styles.PageContent}>
            <p><Link to="/">Back to Main</Link></p>
            <h2 className={styles.AboutHeader}>About</h2>
            <p className={styles.AboutContent}>
                    Piro is an application that assists with rational planning of solid-state synthesis routes for inorganics.
                    It is a recommendation system for navigation and planning of synthesis of inorganic materials based on classical
                    nucleation theory and semi-empirical, data-driven approximations to its parts. Currently it works with Materials Project data via its Rester API.
            </p>
            <p className={styles.AboutContent}>
                    Piro creates synthesis reaction planning plots for target polymorphs under a specific set of thermodynamic
                    conditions and a precursor library, where favorable routes are those that are (nearly) Pareto optimal in terms of two metrics:
                    nucleation barrier and phase-selection. It allows retrosynthetic analysis of target inorganic materials
                    to generate a synthesis reaction tree. (i.e. laying out the reaction pathways necessary to arrive at the
                    target from practical/purchasable reagents/starting materials)
            </p>
            <h4 className={styles.Titles}>Contact</h4>
            <p className={styles.TitlesContent}>
                    The piro platform is developed by a team of researchers and software developers at Toyota Research Institute: Murat Aykol,
                    Joseph Montoya, Jens Hummelshøj, Chris Fajardo, Michael Puzon, and Reko Ong.
                    If you have any questions or feedback, please reach out to us at <a href="mailto:em-piro@tri.global">em-piro@tri.global</a>
            </p>
            <h4 className={styles.Titles}>Code</h4>
            <p className={styles.TitlesContent}>
                    If you’d like to use the python interface to piro, or to access the code for this site,
                    please visit our github page: <a href="https://github.com/TRI-AMDD/piro" target="_blank">https://github.com/TRI-AMDD/piro</a>.
                    Tutorial jupyter notebooks showing how to use piro locally are provided in the notebooks folder.
            </p>
            <h4 className={styles.Titles}>Manuscript</h4>
            <p className={styles.TitlesContent}>
                    For more information about the physical theory behind piro, please read our paper,
                    “Rational Solid-State Synthesis Routes for Inorganic Materials” by Murat Aykol et al.
                    <a href="https://pubs.acs.org/doi/abs/10.1021/jacs.1c04888" target="_blank">(https://pubs.acs.org/doi/abs/10.1021/jacs.1c04888)</a>.
            </p>
        </article>
    );
}
