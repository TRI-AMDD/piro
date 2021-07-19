import styles from './Home.module.css';

interface Props {
    error: object | string;
}

export default function ErrorMessage(props: Props) {
    const { error } = props;
    const errorMessage = typeof error === 'string' ? error : JSON.stringify(error);

    return (
        <div className={styles.Error}>
            <p>Error Message:</p>
            {errorMessage}
        </div>
    );
}
