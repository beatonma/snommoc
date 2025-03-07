import { ReactNode, useCallback, useEffect, useState } from "react";
import { TintedButton } from "@/components/button";
import { GeoLocation } from "@/components/map/geography";
import { ClassNameProps } from "@/types/common";

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
        getCurrentPosition()
          .then(setLocation)
          .catch(handleGetCurrentPositionError);
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

/**
 * Get the user's location only if they have already given permission for it.
 * This is for times when location is a nice-to-have but not worth bothering
 * the user about.
 */
export const usePassiveGeoLocation = (_default?: GeoLocation) => {
  const [location, setLocation] = useState<GeoLocation>();

  useEffect(() => {
    if (!("geolocation" in window.navigator)) return;

    window.navigator.permissions
      .query({ name: "geolocation" })
      .then((status: PermissionStatus) => {
        if (status.state === "granted") {
          getCurrentPosition()
            .then(setLocation)
            .catch(handleGetCurrentPositionError);
        } else {
          setLocation(_default);
        }
      });
  }, []);

  return location;
};

const getCurrentPosition = async () =>
  new Promise<GeoLocation>((resolve, reject) => {
    window.navigator.geolocation.getCurrentPosition(
      (position: GeolocationPosition) => {
        resolve({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        });
      },
      (error) => reject(new Error(`[${error.code}] ${error.message}`)),
      {
        maximumAge: 1000 * 60 * 10, // 10 minutes
      },
    );
  });

const handleGetCurrentPositionError = (e: any) => {
  console.warn(`getCurrentPosition error: ${e}`);
};
