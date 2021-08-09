import { FC } from 'react';
import styles from './Home.module.css';

export type Props = {
    info: string;
    isCheckbox?: boolean;
};

const MoreInfo: FC<Props> = ({ info, isCheckbox, children }) => {
    const style = { marginTop: isCheckbox ? 6 : 16 };

    return (
        <div className={styles.MoreInfo}>
            {children}
            <span className={styles.Tooltip} style={style} data-tip={info}>info</span>
        </div>
    );
};

export default MoreInfo;
