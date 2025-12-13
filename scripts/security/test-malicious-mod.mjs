/**
 * Malicious Mod Test Harness
 * 
 * This script tests cryptographic signature verification to ensure:
 * 1. Artifacts signed by trusted keys are accepted
 * 2. Artifacts signed by untrusted keys are rejected
 * 
 * This is a "test-first" security gate demonstrating supply-chain integrity.
 */

import { writeFileSync, mkdirSync } from "node:fs";
import { createPublicKey, createPrivateKey, generateKeyPairSync, sign, verify } from "node:crypto";
import { join } from "node:path";

function must(condition, message) {
  if (!condition) {
    console.error(`ASSERTION FAILED: ${message}`);
    process.exit(1);
  }
}

function signBytes(privateKeyPem, bytes) {
  const key = createPrivateKey(privateKeyPem);
  return sign(null, bytes, key); // Ed25519 when key is Ed25519
}

function verifyBytes(publicKeyPem, bytes, signature) {
  const key = createPublicKey(publicKeyPem);
  return verify(null, bytes, key, signature);
}

function main() {
  console.log("=== Malicious Mod Security Test ===\n");
  
  const artefactsDir = join("artefacts");
  mkdirSync(artefactsDir, { recursive: true });

  // Generate trusted signer keypair
  console.log("1. Generating trusted signer keypair (Ed25519)...");
  const trusted = generateKeyPairSync("ed25519");
  const trustedPub = trusted.publicKey.export({ type: "spki", format: "pem" });
  const trustedPriv = trusted.privateKey.export({ type: "pkcs8", format: "pem" });

  // Generate untrusted signer keypair (attacker)
  console.log("2. Generating untrusted signer keypair (attacker simulation)...");
  const untrusted = generateKeyPairSync("ed25519");
  const untrustedPriv = untrusted.privateKey.export({ type: "pkcs8", format: "pem" });

  // Create test payload
  const payload = Buffer.from("MOD_PAYLOAD: MCOP Framework Test Module v1.0\n", "utf8");
  console.log(`3. Test payload created: ${payload.length} bytes`);

  // Sign with trusted key
  const goodSig = signBytes(trustedPriv, payload);
  console.log("4. Payload signed with trusted key");

  // Sign with untrusted key (simulating attacker)
  const badSig = signBytes(untrustedPriv, payload);
  console.log("5. Payload signed with untrusted key (attack simulation)");

  // TEST 1: Trusted signature should be accepted
  console.log("\n--- Test 1: Verify trusted signature ---");
  const trustedResult = verifyBytes(trustedPub, payload, goodSig);
  must(trustedResult === true, "Expected trusted signature to verify");
  console.log("✅ PASS: Trusted signature accepted");

  // TEST 2: Untrusted signature should be rejected
  console.log("\n--- Test 2: Reject untrusted signature ---");
  const untrustedResult = verifyBytes(trustedPub, payload, badSig);
  must(untrustedResult === false, "Expected untrusted signature to be rejected");
  console.log("✅ PASS: Untrusted (malicious) signature rejected");

  // TEST 3: Tampered payload should be rejected
  console.log("\n--- Test 3: Reject tampered payload ---");
  const tamperedPayload = Buffer.from("MOD_PAYLOAD: MALICIOUS CODE INJECTED\n", "utf8");
  const tamperedResult = verifyBytes(trustedPub, tamperedPayload, goodSig);
  must(tamperedResult === false, "Expected tampered payload to be rejected");
  console.log("✅ PASS: Tampered payload rejected");

  // Save artifacts for inspection
  writeFileSync(join(artefactsDir, "mod.pak"), payload);
  writeFileSync(join(artefactsDir, "mod.pak.sig"), goodSig);
  writeFileSync(join(artefactsDir, "trusted.pub.pem"), trustedPub);
  console.log(`\n6. Artifacts saved to ${artefactsDir}/`);

  console.log("\n=== Q.E.D. ===");
  console.log("All security tests passed:");
  console.log("  - Malicious signature REJECTED");
  console.log("  - Trusted signature ACCEPTED");
  console.log("  - Tampered payload REJECTED");
  console.log("\nSupply-chain integrity verification: OPERATIONAL");
}

main();
