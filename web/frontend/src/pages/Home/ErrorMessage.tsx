import styles from './Home.module.css';
import { Alert } from "@material-tailwind/react";
import React from 'react';

interface Props {
  error: object | string;
}

export default function ErrorMessage(props: Props) {
  const { error } = props;
  const errorMessage = typeof error === 'string' ? error : JSON.stringify(error);
  const [open, setOpen] = React.useState(true);
 
  return (
    <div className={styles.errortoast}>
      <Alert 
        color="red"
        open={open}
        onClose={() => setOpen(false)}
        animate={{
          mount: { y: 0 },
          unmount: { y: 100 },
        }}
      >
        {errorMessage}
      </Alert>
    </div>
  );
}
