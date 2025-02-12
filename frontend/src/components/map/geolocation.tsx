import { ReactNode, useCallback, useEffect, useState } from "react";
import { TintedButton } from "@/components/button";
import { ClassNameProps } from "@/types/common";

export interface GeoLocation {
  latitude: number;
  longitude: number;
}
interface GeoLocationOptions {
  enabled: boolean;
}
export const useGeoLocation = (options: GeoLocationOptions) => {
  const [location, setLocation] = useState<GeoLocation>();

  useEffect(() => {
    if (!options.enabled) return;
    if (!("geolocation" in window.navigator)) return;

    window.navigator.permissions
      .query({ name: "geolocation" })
      .then((status: PermissionStatus) => {
        if (status.state === "denied") return;
        window.navigator.geolocation.getCurrentPosition(
          (position: GeolocationPosition) => {
            setLocation({
              latitude: position.coords.latitude,
              longitude: position.coords.longitude,
            });
          },
        );
      });
  }, [options.enabled]);

  return location;
};

interface GeoLocationPrompt {
  /**
   * The user's location, if allowed.
   */
  geoLocation: GeoLocation | undefined;

  /**
   * A button element which, when clicked, allows the user to enable geolocation permission.
   * Permission is only requested when the user explicitly clicks this button to allow it.
   * If permission has already been allowed or denied then this will render nothing
   * and no further prompt will follow.
   */
  GeoLocationPromptButton: (props: ClassNameProps) => ReactNode;
}

export const useGeoLocationPrompt = (): GeoLocationPrompt => {
  const [showGeoLocationButton, setShowGeoLocationButton] = useState(false);
  const [isGeoLocationEnabled, setGeoLocationEnabled] = useState(false);
  const geoLocation = useGeoLocation({
    enabled: isGeoLocationEnabled,
  });

  useEffect(() => {
    window.navigator.permissions
      .query({ name: "geolocation" })
      .then((status: PermissionStatus) => {
        switch (status.state) {
          case "denied":
            setShowGeoLocationButton(false);
            break;
          case "granted":
            setGeoLocationEnabled(true);
            break;
          case "prompt":
          default:
            setShowGeoLocationButton(true);
            break;
        }
      });
  }, []);

  const promptButton = useCallback(
    ({ className }: { className?: string | undefined }): ReactNode => {
      if (showGeoLocationButton) {
        return (
          <TintedButton
            onClick={() => {
              setGeoLocationEnabled(true);
              setShowGeoLocationButton(false);
            }}
            className={className}
          >
            Show your location
          </TintedButton>
        );
      }
    },
    [showGeoLocationButton],
  );

  return {
    geoLocation: geoLocation,
    GeoLocationPromptButton: promptButton,
  };
};
