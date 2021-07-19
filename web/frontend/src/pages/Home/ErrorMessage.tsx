import styles from './Home.module.css';

interface Props {
    error: object;
}

export default function ErrorMessage(props: Props) {
    const { error } = props;

    return (
        <div className={styles.Error}>
            <p>Error Message:</p>
            {JSON.stringify(error)}
        </div>
    );
}
