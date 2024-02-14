import TagManager from 'react-gtm-module';

const tagManagerArgs = { gtmId: 'G-QNR2D22FG3' };

TagManager.initialize(tagManagerArgs);

export const infoHandleHover = (event: string, label: string) => {
  window.dataLayer.push({
    event: event,
    label: label
  });
};

export const pushEvent = (event: string) => {
  window.dataLayer.push({
    event: event
  });
};
