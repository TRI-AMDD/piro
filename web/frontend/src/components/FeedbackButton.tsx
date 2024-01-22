// FeedbackButton.tsx

import React from 'react';
import { Button } from '@material-tailwind/react';
import styles from './components.module.css';

interface FeedbackButtonProps {
  showFeedbackButton: boolean;
}

const customStyles = {
              verticalAlign: "align-middle",
              textTransform: "lowercase",

  };

const FeedbackButton: React.FC<FeedbackButtonProps> = () => {
  // Add your feedback button logic here
  return (
    <div className={styles.FeedbackButtonDiv}>
        <Button variant="filled" size="md" textAlign="text-center"  style={{ fontSize: '15px',fontFamily: 'gellix-regular'}} className={`${styles.FeedbackButton} capitalize`} onClick={()=>window.showCollectorDialog()}>
             Feedback
        </Button>
    </div>
  )
};

export default FeedbackButton;
