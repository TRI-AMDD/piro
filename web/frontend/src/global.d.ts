type DataLayerObject =
  | {
      event: string;
      label: string;
    }
  | {
      event: string;
    };

interface Window {
  dataLayer?: DataLayerObject[];
}
