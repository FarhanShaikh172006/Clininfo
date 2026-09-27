// Firebase SDK imports from CDN

import {
    initializeApp,
    getApps,
    getApp
} from "https://www.gstatic.com/firebasejs/12.5.0/firebase-app.js";

import {
    getAuth
} from "https://www.gstatic.com/firebasejs/12.5.0/firebase-auth.js";

import {
    getFirestore
} from "https://www.gstatic.com/firebasejs/12.5.0/firebase-firestore.js";


// Initialize Firebase

export function initFirebase(config) {

    if (!config || !config.apiKey) {
        throw new Error("Firebase configuration is missing.");
    }


    // Prevent Firebase from being initialized multiple times

    const app = getApps().length > 0
        ? getApp()
        : initializeApp(config);


    // Firebase Authentication

    const auth = getAuth(app);


    // Cloud Firestore

    const db = getFirestore(app);


    return {
        app,
        auth,
        db
    };
}