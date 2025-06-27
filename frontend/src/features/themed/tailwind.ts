import { HouseType } from "@/api/schema";

export const houseSurface = (house: HouseType) => {
  switch (house) {
    case "Commons":
      return "surface-commons";
    case "Lords":
      return "surface-lords";
  }
};
