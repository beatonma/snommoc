export type Nullish = null | undefined;

/**
 * Symmetric difference of types A and B.
 * XOR<A, B> can have attributes from A, or from type B, but not both.
 */
export type XOR<A, B> =
  | (A & { [K in Exclude<keyof B, keyof A>]?: never })
  | (B & { [K in Exclude<keyof A, keyof B>]?: never });

export type NullableValues<T> = { [K in keyof T]: T[K] | Nullish };
